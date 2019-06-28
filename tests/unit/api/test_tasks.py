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

import uuid
from mock import Mock
import datetime
import json
from orchestration.connectionmanager.st2 import St2


def test_tasks_output(client):
    id = str(uuid.uuid4())
    url = '/v1beta/orchestration/tasks' + id
    response = client.get(url)
    assert response.status_code == 404


def test_tasks_no_exec_id(client):
    response = client.get('/v1beta/orchestration/tasks')
    assert response.status_code == 404


def test_get_task_status(client, monkeypatch):
    id = str(uuid.uuid4())
    url = '/v1beta/xyz/orchestration/tasks/' + id
    # Form the data to be mocked
    data = {}
    data['id'] = id
    data['start_timestamp'] = str(datetime.datetime.now())
    data['end_timestamp'] = str(datetime.datetime.now())
    data['status'] = 'Success'
    temp = {}
    temp['tasks'] = []
    data['result'] = temp

    St2.get_execution_stats = Mock(return_value=(200, json.dumps(data)))
    response = client.get(url)
    assert response.status_code == 200


def test_get_task_status_invalid(client):
    id = str(uuid.uuid4())
    url = '/v1beta/xyz/orchestration/tasks/' + id
    # Form the data to be mocked
    data = {}
    St2.get_execution_stats = Mock(return_value=(200, json.dumps(data)))
    response = client.get(url)
    assert response.status_code == 404
