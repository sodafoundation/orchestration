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
from orchestration.utils.config import logger

task = Blueprint("task", __name__)


@task.route(
    "/v1beta/<string:tenant_id>/orchestration/tasks/<string:exec_id>",
    methods=['GET'])
def get_task_status(tenant_id='', exec_id=''):
    c = Connector().morph()
    rc, ret = c.get_execution_stats(exec_id)
    if(rc != Apiconstants.HTTP_OK):
        return jsonify(response=json.loads(ret)), rc

    try:
        ret_json = json.loads(ret)
        task_hash = {}
        task_hash['id'] = ret_json['id']
        task_hash['start'] = ret_json['start_timestamp']
        if 'end_timestamp' in ret_json:
            task_hash['end'] = ret_json['end_timestamp']
        if 'status' in ret_json:
            task_hash['status'] = ret_json['status']
        published_res = {}
        if 'result' in ret_json:
            result = ret_json['result']
            for tasks in result['tasks']:
                published_res.update(tasks['published'])
            task_hash['published'] = published_res
    except Exception as ex:
        logger.error(
                        "Received exception in getting task status: {}"
                        .format(ex.message))
        return jsonify(
                        Apiconstants.TASK_ERR_MSG
                    ), Apiconstants.HTTP_ERR_NOTFOUND
    return jsonify(task_hash), 200
