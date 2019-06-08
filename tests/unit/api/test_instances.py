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

import json
import uuid


def test_post_instance(client):
    type_mime = 'application/json'
    header = {'Content-Type': type_mime, 'Accept': type_mime}
    data = {
        "service_id": "26ab0773-fc5a-4211-a8e9-8e61ff16fa42",
        "action": "opensds.migration-bucket",
        "name": "foo",
        "parameters": {
            "ip_addr": "1.2.3.4",
            "port": "8089",
            "tenant_id": "7fc5d",
            "userId": "648e3089",
            "name": "testmigration",
            "description": "Migration_test_orchestration",
            "destBackend": "hw-backend",
            "srcBucketName": "aws-orchestrate",
            "destBucketName": "hw-orchestrate",
            "auth_token": "abcde"
        }
    }
    url = '/v1beta/xyz/orchestration/instances'
    response = client.post(url, data=json.dumps(data), headers=header)
    assert response.status_code == 500


def test_list_instance(client):
    response = client.get('/v1beta/xyz/orchestration/instances')
    assert response.status_code == 200


def test_list_instance_wrong_url(client):
    response = client.get('/v1beta/xyz/orchestration/nstances')
    assert response.status_code == 404


def test_get_instance_by_id(client):
    id = str(uuid.uuid4())
    url = '/v1beta/xyz/orchestration/instances/' + id
    response = client.get(url)
    assert response.json == {}


# mock the return of any function
def mockreturn(self='', id='', name=''):
    return 200, []


def test_delete_instance(client, monkeypatch):
    id = str(uuid.uuid4())
    url = '/v1beta/xyz/orchestration/' + id
    response = client.delete(url)
    # This should return 404 error as the ID is not present
    assert response.status_code == 404


def test_put_instance(client, monkeypatch):
    id = str(uuid.uuid4())
    url = '/v1beta/xyz/orchestration/' + id
    type_mime = 'application/json'
    header = {'Content-Type': type_mime, 'Accept': type_mime}
    data = {}
    response = client.put(url, data=json.dumps(data), headers=header)
    # This should return 404 error as the ID is not present
    assert response.status_code == 404


def test_get_instance(client):
    response = client.get('/v1beta/xyz/orchestration/instances/a1bcd')
    assert response.status_code == 404
