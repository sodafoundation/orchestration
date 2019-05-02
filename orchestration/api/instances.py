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
from orchestration.connectionmanager.Connector import connector
from flask import request
import json
from orchestration.db.api \
    import create_workflow_definition, get_workflow_definition

instance = Blueprint("instance", __name__)

# API to execute a service.
# For example, St2 execution of this API will require 'action'
# as one of the parameter. 'parameters' maybe required for the Actions
# St2 example of data:/v1beta/orchestration/instances -H
# "Content-Type:application/json" -d
# '{"action":"aks.ak_echo_py", "parameters":{"message":"Hello World"}}'
@instance.route("/v1beta/orchestration/instances", methods=['POST'])
def instance_ops():
    c = connector().morph()
    content = request.get_json()
    ret = c.execute_action(content)
    ret_json = json.loads(ret)
    return jsonify(response=json.dumps(ret_json)), 200


@instance.route("/v1beta/orchestration/workflow", methods=['POST'])
def create_action():
    c = connector().morph()
    content = request.get_json()
    ret = c.create_action(content)
    return jsonify(response=json.dumps(ret)), 200


@instance.route(
    "/v1beta/orchestration/workflow/<string:id>",
    methods=['GET', 'PUT', 'DELETE'])
def wf_ops(id=''):
    c = connector().morph()
    method = request.method
    if method == 'GET':
        ret = c.list_actions(id)
        wf_hash = {}
        wfs = []
        for elem in ret.values():
            if elem['runner_type'] == 'mistral-v2':
                wfd_hash = {}
                wfd_hash['id'] = elem['ref']
                wfd_hash['name'] = elem['name']
                wfd_hash['description'] = elem['description']
                wfd_hash['definition'] = json.dumps(elem['parameters'])
                # check if the entries are not present in DB then only
                # enter in DB
                wfs.append(wfd_hash)
                if get_workflow_definition(None, elem['ref']) is None:
                    create_workflow_definition(None, wfd_hash)
        wf_hash['workflows'] = wfs
        return jsonify(id=id, response=wfs), 200
    elif method == 'PUT':
        content = request.get_json()
        ret = c.update_action(id, content)
        return jsonify(response=json.dumps(ret)), 200
    elif method == 'DELETE':
        content = request.get_json()
        ret = c.delete_action(id, content)
        return jsonify(response=json.dumps(ret)), 200
