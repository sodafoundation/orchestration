# Copyright 2019 The OpenSDS Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import boto3
import time

from st2common.runners.base_action import Action

RET_SUCCEED = "success"
RET_FAILED = "failed"


# format of args:
# {
#   'Name': 'string'
#   'AK': 'string'
#   'SK': 'string'
#   'Region': 'string'  #example: 'us-east-1'
#   'ReleaseLabel': 'string'   #example: 'emr-5.20.0'
#   'Instances': {
#       'MasterInstanceType': 'string'   #example: 'm3.xlarge'
#       'SlaveInstanceType': 'string'   #example: 'm3.xlarge'
#       'InstanceCount': 123   #example: 4 (means 1 master node and 3 slave nodes)
#       'KeepJobFlowAliveWhenNoSteps': True|False
#       'TerminationProtected': True|False
#   }
#   'JobFlowRole': 'string'   #example: 'EMR_EC2_DefaultRole'
#   'ServiceRole': 'string'   #example: 'EMR_DefaultRole'
#   'VisibleToAllUsers': True|False
#   'Applications': [
#       {
#           'Name': 'string'   #example: 'Hadoop'
#       }
#   ]
#   'Steps': [
#       {
#           'Name': 'string'
#           'ActionOnFailure': 'TERMINATE_JOB_FLOW'|'TERMINATE_CLUSTER'|'CANCEL_AND_WAIT'|'CONTINUE'
#           'HadoopJarStep': {
#               'Jar': 'string'   #example: 's3n://elasticmapreduce/samples/cloudfront/logprocessor.jar' or
#               'command-runner.jar'
#               'Args':['string']   #example: ['-input', 's3n://mytest/analysis_bucket/input', '-output',
#               's3n://mytest/analysis_bucket/output'] or ['state-pusher-script']
#           }
#       }
# ]
# }


class ExecAnalysisAction(Action):
    def run(self, analysis_engine_type="", args="", auth_token=""):
        ret = RET_SUCCEED
        if analysis_engine_type == 'aws emr':
            status = aws_analysis(args)
            if status != 'SUCCEED':
                ret = RET_FAILED
        else:
            print("unsupported analysis engine type:%s" % analysis_engine_type)
            ret = RET_FAILED

        return ret


def get_job_end_status(client, jid):
    status = 'FAILED'
    while True:
        # get status each 30 seconds
        time.sleep(30)
        resp = client.describe_cluster(ClusterId=jid)
        print(resp)
        # value for State:
        # 'STARTING'|'BOOTSTRAPPING'|'RUNNING'|'WAITING'|'TERMINATING'|'TERMINATED'|'TERMINATED_WITH_ERRORS'
        state = resp.get("Cluster").get("Status").get("State")
        # value of StateChangeReason.Code: INTERNAL_ERROR | VALIDATION_ERROR |
        # INSTANCE_FAILURE | INSTANCE_FLEET_TIMEOUT | BOOTSTRAP_FAILURE |
        # USER_REQUEST | STEP_FAILURE | ALL_STEPS_COMPLETED
        if state == 'TERMINATED' or state == 'TERMINATED_WITH_ERRORS':
            terminateCode = resp.get("Cluster").get(
                "Status").get("StateChangeReason").get("Code")
            print("job terminate state: %s" % state)
            print("job terminate reason: %s" % terminateCode)
            if terminateCode == 'ALL_STEPS_COMPLETED':
                status = 'SUCCEED'
            break

    return status


def aws_analysis(args):
    # create a client
    client = boto3.client(
        'emr',
        aws_access_key_id=args['AK'],
        aws_secret_access_key=args['SK'],
        region_name=args["Region"]
    )

    apps = []
    for app in args['Applications']:
        apps.append(app)

    steps = []
    for step in args['Steps']:
        steps.append(step)

    count = args['Instances']['InstanceCount']
    instances = {
        'InstanceCount': count,
        'MasterInstanceType': args['Instances']['MasterInstanceType'],
        'KeepJobFlowAliveWhenNoSteps': False,  # TODO: support True
        'TerminationProtected': False,  # TODO: support True
    }
    if count > 1:
        instances['SlaveInstanceType'] = args['Instances']['SlaveInstanceType']

    response = client.run_job_flow(
        Name=args['Name'],
        ReleaseLabel=args['ReleaseLabel'],
        Instances=instances,
        JobFlowRole=args['JobFlowRole'],
        ServiceRole=args['ServiceRole'],
        VisibleToAllUsers=args['VisibleToAllUsers'],
        Applications=apps,
        Steps=steps
    )

    # get returned status
    # response example: {'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200,
    # 'RequestId': '026ec48e-8da3-11e9-baa7-5170a521c0b0',
    # 'HTTPHeaders': {'x-amzn-requestid': '026ec48e-8da3-11e9-baa7-5170a521c0b0',
    # 'date': 'Thu, 13 Jun 2019 06:18:07 GMT', 'content-length': '31',
    # 'content-type': 'application/x-amz-json-1.1'}}, u'JobFlowId': u'j-3IVHGVODNQK78'}
    http_code = response['ResponseMetadata']['HTTPStatusCode']
    if http_code != 200:
        print("aws emr: run job flow failed, http_code is %d" % http_code)
        raise RuntimeError('run aws emr job flow failed')

    print(response)

    flowid = response['JobFlowId']
    final_status = get_job_end_status(client, flowid)
    if final_status != 'SUCCEED':
        print(
            "aws emr: job flow run failed, id=%s, job_status=%s" %
            (flowid, final_status))
        raise RuntimeError('aws emr job run failed')

    print("aws emr: job flow run succeed, id=%s" % flowid)
