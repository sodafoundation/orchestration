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
import json
from orchestration.api.apiconstants import Apiconstants

task = Blueprint("task", __name__)
@task.route("/v1/orchestration/tasks/<string:execId>", methods=['GET'])
def get_task_output(execId=''):
    c = Connector().morph()
    rc, ret = c.get_execution_stats(execId)
    if(rc != Apiconstants.HTTP_OK):
        return jsonify(response=json.loads(ret)), rc

    ret_json = json.loads(ret)
    task_hash = {}
    task_hash['id'] = ret_json['id']
    task_hash['start'] = ret_json['start_timestamp']
    task_hash['end'] = ret_json['end_timestamp']
    task_hash['status'] = ret_json['status']
    task_hash['message'] = 'Failed'
    if ret_json['status'] == 'succeeded':
        task_hash['message'] = ret_json['result']['tagline']
    return jsonify(response=task_hash), 200
