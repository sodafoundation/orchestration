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

import pytest
import uuid
from orchestration.server import server_manager
from orchestration.connectionmanager.st2 import St2
from mock import Mock, patch
import json


@pytest.fixture
def client():
    server_manager.app.config['TESTING'] = True
    client = server_manager.app.test_client()

    yield client


# Fixture to prevent "requests" library from performing
# http requests. reference: https://docs.pytest.org/en/3.0.1/monkeypatch.html
@pytest.fixture(autouse=False)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.session.Session.request")


def mockreturn(self=''):
    return ''


@pytest.fixture(autouse=False)
def mock_list_services(self=''):
    id = str(uuid.uuid4())
    service_ret = []
    service = {}
    service['id'] = id
    service['input'] = ''
    service_ret.append(service)
    mock = Mock(return_value=service_ret)
    patch('orchestration.db.api.list_services', mock)


@pytest.fixture(autouse=False)
def mock_exec_stats(self=''):
    stats_ret = {}
    stats_ret['status'] = 'succeeded'
    St2.get_execution_stats = Mock(return_value=(200, json.dumps(stats_ret)))


@pytest.fixture(autouse=False)
def mock_exec_output(self=''):
    output_ret = {}
    output_ret['output'] = ''
    St2.get_execution_output = Mock(return_value=(200, json.dumps(output_ret)))


@pytest.fixture(autouse=True)
def no_om_authenticate(monkeypatch):
    monkeypatch.setattr("orchestration.connectionmanager.st2.St2.authenticate",
                        mockreturn)
