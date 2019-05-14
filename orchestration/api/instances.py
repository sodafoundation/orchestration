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
    import create_workflow, list_workflows
from orchestration.api.apiconstants import Apiconstants
from orchestration.utils.config import logger

instance = Blueprint("instance", __name__)

# API to execute a service.
# For example, St2 execution of this API will require 'action'
# as one of the parameter. 'parameters' maybe required for the Actions
# St2 example of data:/v1beta/orchestration/instances -H
# "Content-Type:application/json" -d
# '{"action":"aks.ak_echo_py", "parameters":{"message":"Hello World"}}'
@instance.route("/v1beta/orchestration/instances", methods=['POST'])
def instance_ops():
    c = Connector().morph()
    content = request.get_json()
    rc, ret = c.execute_action(content)
    if(rc != Apiconstants.HTTP_CREATED):
        logger.error("api response received return code[%d]", rc)
        return jsonify(json.loads(ret)), rc

    ret_json = json.loads(ret)
    wf_hash = {}
    wf_hash['id'] = ret_json['id']
    wf_hash['name'] = ret_json['action']['name']
    wf_hash['input'] = json.dumps(ret_json['parameters'])
    wf_hash['workflow_source'] = ret_json['action']['ref']
    # Create the record of this instance in DB
    logger.info("creating workflow table with record [%s]", str(wf_hash))
    create_workflow(None, wf_hash)
    return jsonify(ret_json), 200


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


@instance.route(
    "/v1beta/orchestration/instances",
    methods=['GET', 'PUT', 'DELETE'])
def wf_ops():
    c = Connector().morph()
    method = request.method
    if method == 'GET':
        logger.info("inside getting actions")
        ret = list_workflows(None)
        logger.debug("returning list of workflows: %s" % (ret))
        return jsonify(ret), 200
    elif method == 'PUT':
        content = request.get_json()
        rc, ret = c.update_action(id, content)
        if(rc != Apiconstants.HTTP_OK):
            return jsonify(json.loads(ret)), rc

        return jsonify(json.dumps(ret)), 200
    elif method == 'DELETE':
        content = request.get_json()
        rc, ret = c.delete_action(id, content)
        if(rc != Apiconstants.HTTP_OK):
            return jsonify(json.loads(ret)), rc

        return jsonify(json.dumps(ret)), 200
