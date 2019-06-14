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


def test_list_service(client):
    response = client.get('/orchestration/xyz/services')
    assert response.status_code == 200


def test_get_service(client):
    id = str(uuid.uuid4())
    url = '/orchestration/xyz/services' + id
    response = client.get(url)
    assert response.status_code == 404
