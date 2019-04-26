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
# from flask import request

service = Blueprint("service", __name__)


# This API will provide the details of the action 'id' provided
@service.route("/v1/orchestration/services/<string:id>", methods=['GET'])
def get_service(id=''):
    c = Connector().morph()
    ret = c.listActions(id)
    return jsonify(id=id, response=ret), 200
