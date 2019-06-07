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
from utils import OPENSDS_IP, OPENSDS_TOKEN, get_project_id, get_url


# API get instances
def get_instances():
    url = get_url() + "instances"
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Instance list failed", resp.status_code)

    print(resp.text)


# API run instance
def run_instance(service_id):
    url = get_url() + "instances"
    headers = {
        'content-type': 'application/json'
    }

    data = {
        "id": service_id,
        "action": "opensds.provision-volume",
        "parameters":
            {
                "ip_addr": OPENSDS_IP,
                "port": "50040",
                "tenant_id": get_project_id(),
                "size": 1,
                "name": "full",
                "auth_token": OPENSDS_TOKEN
            }
    }

    print(data)
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    if resp.status_code != 200:
        print(
            "Request for Run Provision Volume Services failed",
            resp.status_code)

    print(resp.text)
