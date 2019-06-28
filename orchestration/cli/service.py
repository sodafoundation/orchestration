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
from utils import get_url


# API get service from id
def get_services(args):
    if args.id is None:
        raise Exception('Missing parameter, "id"')
    url = get_url(args.project_id) + "services/" + args.id
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Service failed", resp.status_code)

    print(json.dumps(resp.json(), indent=2, sort_keys=True))


# API get services
def list_services(args):
    url = get_url(args.project_id) + "services"
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Services list failed", resp.status_code)

    print(json.dumps(resp.json(), indent=2, sort_keys=True))


# API register services
# Example Input data JSON format
# {
#     "name":"volume provision",
#     "description":"Volume Service",
#     "tenant_id":"94b280022d0c4401bcf3b0ea85870519",
#     "user_id":"558057c4256545bd8a307c37464003c9",
#     "input":"",
#     "constraint":"",
#     "group":"provisioning",
#     "workflows":[
#         {
#             "definition_source":"opensds.provision-volume",
#             "wfe_type":"st2"
#         },
#         {
#             "definition_source":"opensds.snapshot-volume",
#             "wfe_type":"st2"
#         }
#     ]
# }

def add_services(args):
    if args.data is None:
        raise Exception('Missing parameter, "data"')
    url = get_url(args.project_id) + "services"
    headers = {
        'content-type': 'application/json'
    }

    resp = requests.post(url=url, data=json.dumps(args.data), headers=headers)
    if resp.status_code != 200:
        print("Request for Register Services failed", resp.status_code)

    print(json.dumps(resp.json(), indent=2, sort_keys=True))
