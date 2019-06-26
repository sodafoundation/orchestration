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
from utils import get_url, get_opensds_token


# API get instances
def get_instances(args):
    url = get_url(args.project_id) + "instances"
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Instance list failed", resp.status_code)

    print(resp.text)


# API run instance
# Example Input data JSON format
# {
#   "service_id": "08e8a8a3-7a78-43d3-9ab1-45fe7a60d4eb",
#   "action": "opensds.provision-volume",
#   "name": "Volume Provision name",
#   "description": "Volume Provision description",
#   "user_id": "558057c4256545bd8a307c37464003c9",
#   "parameters": {
#     "ip_addr": "127.0.0.1",
#     "port": "50040",
#     "tenant_id": "94b280022d0c4401bcf3b0ea85870519",
#     "size": 1,
#     "name": "test",
#   }
# }

def run_instance(args):
    if args.data is None:
        raise Exception('Missing parameter, "data"')
    url = get_url(args.project_id) + "instances"
    headers = {
        'content-type': 'application/json',
        'x-auth-token': get_opensds_token()
    }

    resp = requests.post(url=url, data=args.data, headers=headers)
    if resp.status_code != 200:
        print(
            "Request for Run Provision Volume Services failed",
            resp.status_code)

    print(resp.text)
