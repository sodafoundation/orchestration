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

from flask import jsonify
from flask import Blueprint
from orchestration.connectionmanager.connector import Connector
from flask import request
import json
from orchestration.db.api \
    import create_workflow, list_workflows, create_service, \
    get_sd_wfd_association, get_workflow, delete_workflow, get_wf_sd
from orchestration.api.apiconstants import Apiconstants
from orchestration.utils.config import logger

instance = Blueprint("instance", __name__)

# API to execute a service.
# For example, St2 execution of this API will require 'action'
# as one of the parameter. 'parameters' maybe required for the Actions
# St2 example of data:/v1beta/orchestration/instances -H
# "Content-Type:application/json" -d
# '{"action":"aks.ak_echo_py", "parameters":{"message":"Hello World"}}'
@instance.route("/v1beta/<string:tenant_id>/orchestration/instances",
                methods=['POST'])
def instance_ops(tenant_id=''):
    c = Connector().morph()
    content = request.get_json()
    # get the service_definition id from the content and remove this from data
    sd_id = content['id']
    del content['id']
    content['parameters']['tenant_id'] = tenant_id
    try:
        rc, ret = c.execute_action(content)
        if(rc != Apiconstants.HTTP_CREATED):
            logger.error("api response received return code[%d]", rc)
            return jsonify(json.loads(ret)), rc
    except Exception as ex:
        # The requests may throw ConnectionError. Handle it
        logger.error("recieved exception [%s] while executing action", str(ex))
        return jsonify([]), 500

    ret_json = json.loads(ret)

    # creat service attribs from the return
    service_map = {}
    service_map['name'] = ret_json['action']['name']
    service_map['input'] = json.dumps(ret_json['parameters'])
    # get the service definition id
    service_map['service_definition_id'] = sd_id
    service_obj = create_service(None, service_map)

    wf_hash = {}
    wf_hash['id'] = ret_json['id']
    wf_hash['name'] = ret_json['action']['name']
    wf_hash['input'] = json.dumps(ret_json['parameters'])
    wf_hash['workflow_source'] = ret_json['action']['ref']
    wf_hash['service_id'] = service_obj['id']

    wd_id = ''
    try:
        service_wf_list = get_sd_wfd_association(None, sd_id)
        if not service_wf_list or service_wf_list is None:
            logger.info("could not get workflow definition for sd %s", sd_id)
        else:
            for sd, wd in service_wf_list:
                wd_id = wd.id
    except Exception as e:
        logger.error("received exception while getting wfd id %s", str(e))

    wf_hash['workflow_definition_id'] = wd_id

    # Create the record of this instance in DB
    logger.info("creating workflow table with record [%s]", str(wf_hash))

    # Create a Service of this execution.
    create_workflow(None, wf_hash)
    return jsonify(wf_hash), 200


'''
Internal API to get the Workflow definitions
This can be imported and called directly from
outside
'''


def get_wfds():
    c = Connector().morph()
    ret = c.list_actions('opensds')
    logger.debug("returning list of actions: %s" % (ret))
    return ret


# This to get the Workflow definition from st2
def get_wfd(id):
    c = Connector().morph()
    rc, ret = c.get_action(id, 'opensds')
    if rc != Apiconstants.HTTP_OK:
        logger.error("api response return error code [%d]", rc)
        return None
    return ret


@instance.route(
    "/v1beta/orchestration/workflows",
    methods=['GET'])
def wfds_ops():
    ret = get_wfds()
    return jsonify(ret), 200


# Get all the instances of a particular service definition
@instance.route(
    "/v1beta/orchestration/instances/service/<string:service_def_id>",
    methods=['GET'])
def get_instance_sd(service_def_id=''):
    # Query the db and return result
    ret = ''
    try:
        ret = get_wf_sd(service_def_id)
    except Exception as ex:
        logger.error("error in getting result for sd [%s]", str(ex))
        return jsonify(ret), 400
    try:
        # Create a hash of Service Definition Id and the Wfs
        sd_wf_hash = {}
        wf_list = []
        for wf, service in ret:
            # Create a hash of all the WFs
            wf_hash = {}
            wf_hash['id'] = wf.id,
            wf_hash['name'] = wf.name,
            wf_hash['input'] = json.loads(wf.input),
            wf_hash['workflow_source'] = wf.workflow_source,
            wf_hash['service_id'] = wf.service_id,
            wf_hash['workflow_definition_id'] = wf.workflow_definition_id
            # Add the Wfs to the List
            wf_list.append(wf_hash)

        sd_wf_hash[service_def_id] = wf_list
    except Exception as ex:
        logger.error("error in getting the WFs for SD [%s]: \
            [%s]" % (service_def_id, str(ex)))
    return jsonify(sd_wf_hash), 200


@instance.route(
    "/v1beta/<string:tenant_id>/orchestration/instances/<string:instance_id>",
    methods=['GET', 'PUT', 'DELETE'])
@instance.route(
    "/v1beta/<string:tenant_id>/orchestration/instances",
    methods=['GET'])
def wf_ops(tenant_id='', instance_id=''):
    c = Connector().morph()
    method = request.method
    if method == 'GET':
        logger.info("inside getting actions")
        if instance_id == '':
            ret = list_workflows(None)
        else:
            ret = get_workflow(None, instance_id)
        logger.debug("returning list of workflows: %s" % (ret))
        return jsonify(ret), 200
    elif method == 'PUT':
        content = request.get_json()
        content['parameters']['tenant_id'] = tenant_id
        rc, ret = c.update_action(id, content)
        if(rc != Apiconstants.HTTP_OK):
            return jsonify(json.loads(ret)), rc

        return jsonify(json.dumps(ret)), 200
    elif method == 'DELETE':
        rc, ret = c.delete_action(instance_id)
        if(rc != Apiconstants.HTTP_OK):
            return jsonify(json.loads(ret)), rc
        # once the instance is deleted, delete it from DB too
        try:
            delete_workflow(None, instance_id)
        except Exception as e:
            logger.error("error while deleting instance %s from db", str(e))

        return jsonify(json.dumps(ret)), 200
