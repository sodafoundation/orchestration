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
from requests.auth import HTTPBasicAuth
import json

# Input parameters
OPENSDS_IP = "100.64.41.212"
OPENSDS_TOKEN = ''  # Insert token here
ORCHESTRATOR_IP = "localhost"
ORCHESTRATOR_PORT = '5000'
ST2_USER = 'st2admin'
ST2_PASSWORD = 'lbBIIK3P'
ST2_HOST = "localhost"


def get_info():
    print("project_id:", get_project_id())


def get_project_id():
    url = "http://" + OPENSDS_IP + "/identity/v3/projects"
    headers = {
        'x-auth-token': OPENSDS_TOKEN
    }
    resp = requests.get(url=url, headers=headers)
    if resp.status_code != 200:
        print("Request for Project ID failed", resp.status_code)

    json_resp = json.loads(resp.text)

    for proj in json_resp['projects']:
        if proj['name'] == 'admin':
            print("OpenSDS Project ID =", proj['id'])
            return proj['id']

    print("ERROR: Failed to get project ID")
    return ''


def get_user_id():
    url = "http://" + OPENSDS_IP + "/identity/v3/users"
    headers = {
        'x-auth-token': OPENSDS_TOKEN
    }
    resp = requests.get(url=url, headers=headers)
    if resp.status_code != 200:
        print("Request for Project ID failed", resp.status_code)

    json_resp = json.loads(resp.text)

    for usr in json_resp['users']:
        if usr['name'] == 'admin':
            print("OpenSDS User ID =", usr['id'])
            return usr['id']

    print("ERROR: Failed to get user ID")
    return ''


def get_st2_token():
    url = "https://" + ST2_HOST + "/auth/v1/tokens"
    headers = {
        'content-type': 'application/json'
    }
    auth = HTTPBasicAuth(ST2_USER, ST2_PASSWORD)
    resp = requests.post(url=url, auth=auth, headers=headers, verify=False)
    if resp.status_code != 201:
        print("Request for ST2 Token failed")
    json_resp = json.loads(resp.text)
    tok = json_resp['token']
    print("StackStorm token is: ", tok)
    return tok


def get_opensds_token():
    url = "http://" + OPENSDS_IP + "/identity/v3/auth/tokens"
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": "admin",
                        "domain": {"id": "default"},
                        "password": "opensds@123"
                    }
                }
            }
        }
    }
    resp = requests.post(
        url=url, data=json.dumps(data), headers=headers, verify=False)
    if resp.status_code != 201:
        print("Request for OpenSDS Token failed ", resp.status_code)

    print("OpenSDS Token: ", resp.headers['X-Subject-Token'])
    return resp.headers['X-Subject-Token']


def get_url():
    return(
        "http://" + ORCHESTRATOR_IP +
        ":" + ORCHESTRATOR_PORT +
        "/v1beta/" + get_project_id() +
        "/orchestration/")
