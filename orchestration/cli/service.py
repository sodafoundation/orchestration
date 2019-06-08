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

# This class contains the constants required by different modules

import requests
import json
from utils import get_project_id, get_user_id, get_url


# API get service from id
def get_services(service_id):
    url = get_url() + "services/" + service_id
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Service failed", resp.status_code)

    print(resp.text)


# API get services
def list_services():
    url = get_url() + "services"
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Services list failed", resp.status_code)

    print(resp.text)


# API register services
def add_services():
    url = get_url() + "services"
    headers = {
        'content-type': 'application/json'
    }

    data = {
        "name": "volume provision",
        "description": "Volume Service",
        "tenant_id": get_project_id(),
        "user_id": get_user_id(),
        "input": "",
        "constraint": "",
        "group": "provisioning",
        "workflows": [
            {
                "definition_source": "opensds.provision-volume",
                "wfe_type": "st2"
            },
            {
                "definition_source": "opensds.snapshot-volume",
                "wfe_type": "st2"
            }

        ]

    }
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    if resp.status_code != 200:
        print("Request for Register Services failed", resp.status_code)

    print(resp.text)
