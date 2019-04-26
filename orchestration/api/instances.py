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
from flask import request
import json

instance = Blueprint("instance", __name__)

# API to execute a service.
# For example, St2 execution of this API will require 'action'
# as one of the parameter. 'parameters' maybe required for the Actions
# St2 example of data:/v1/orchestration/instances -H
# "Content-Type:application/json" -d
# '{"action":"aks.ak_echo_py", "parameters":{"message":"Hello World"}}'
@instance.route("/v1/orchestration/instances", methods=['POST'])
def execute_service():
    c = Connector().morph()
    content = request.get_json()
    ret = c.executeAction(content)
    return jsonify(response=json.dumps(ret)), 200
