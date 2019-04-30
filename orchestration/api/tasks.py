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
from orchestration.connectionmanager.Connector import Connector
import json

task = Blueprint("task", __name__)
@task.route("/v1/orchestration/tasks/<string:execId>", methods=['GET'])
def get_task_output(execId=''):
    c = Connector().morph()
    ret = c.get_execution_stats(execId)
    return jsonify(response=json.dumps(ret)), 200
