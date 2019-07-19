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
OPENSDS_IP = "127.0.0.1"
OPENSDS_PORT = "50040"
OPENSDS_USER = 'admin'
OPENSDS_PASS = 'opensds@123'
ORCHESTRATOR_IP = "localhost"
ORCHESTRATOR_PORT = '5000'
ST2_USER = 'st2admin'
ST2_PASSWORD = ''
ST2_HOST = "localhost"


def update_config_vars(args):
    global OPENSDS_IP
    global OPENSDS_USER
    global OPENSDS_PASS
    global ORCHESTRATOR_IP
    global ORCHESTRATOR_PORT

    if args.address is not None:
        OPENSDS_IP = args.address
    if args.user is not None:
        OPENSDS_USER = args.user
    if args.password is not None:
        OPENSDS_PASS = args.password
    if args.password is not None:
        ORCHESTRATOR_IP = args.orch_ip
    if args.password is not None:
        ORCHESTRATOR_PORT = args.orch_port


def get_info(ip, user, password):
    global OPENSDS_IP
    global OPENSDS_PORT
    print("OPENSDS_IP:", OPENSDS_IP)
    print("OPENSDS_PORT:", OPENSDS_PORT)
    global OPENSDS_USER
    global OPENSDS_PASS
    print("OPENSDS_USER:", OPENSDS_USER)
    print("OPENSDS_PASS:", OPENSDS_PASS)
    global ORCHESTRATOR_IP
    global ORCHESTRATOR_PORT
    print("ORCHESTRATOR_IP:", ORCHESTRATOR_IP)
    print("ORCHESTRATOR_PORT:", ORCHESTRATOR_PORT)
    global ST2_USER
    global ST2_PASSWORD
    global ST2_HOST
    print("ST2_USER:", ST2_USER)
    print("ST2_PASSWORD:", ST2_PASSWORD)
    print("ST2_HOST:", ST2_HOST)

    token = get_opensds_token(ip, user, password)
    print("token_id:", token)
    print("project_id:", get_project_id(ip, user, token))
    print("user_id:", get_user_id(ip, user, token))


def get_project_id(ip, user, token):
    url = "http://" + ip + "/identity/v3/projects"
    headers = {
        'x-auth-token': token
    }
    resp = requests.get(url=url, headers=headers)
    if resp.status_code != 200:
        raise Exception('Request for Project ID failed')

    json_resp = json.loads(resp.text)

    for proj in json_resp['projects']:
        if proj['name'] == user:
            return proj['id']

    raise Exception('No project ID in response')


def get_user_id(ip, user, token):
    url = "http://" + ip + "/identity/v3/users"
    headers = {
        'x-auth-token': token
    }
    resp = requests.get(url=url, headers=headers)
    if resp.status_code != 200:
        raise Exception('Request for User ID failed')

    json_resp = json.loads(resp.text)

    for usr in json_resp['users']:
        if usr['name'] == user:
            return usr['id']

    raise Exception('No User ID in response')


def get_st2_token():
    url = "https://" + ST2_HOST + "/auth/v1/tokens"
    headers = {
        'content-type': 'application/json'
    }
    auth = HTTPBasicAuth(ST2_USER, ST2_PASSWORD)
    resp = requests.post(url=url, auth=auth, headers=headers, verify=False)
    if resp.status_code != 201:
        raise Exception('Request for ST2 Token failed')

    json_resp = json.loads(resp.text)
    tok = json_resp['token']
    print("StackStorm token is: ", tok)
    return tok


def get_opensds_token(ip=OPENSDS_IP, user=OPENSDS_USER, password=OPENSDS_PASS):
    url = "http://" + ip + "/identity/v3/auth/tokens"
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": user,
                        "domain": {"id": "default"},
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": "default"
                    },
                    "name": user
                }
            }
        }
    }
    resp = requests.post(
        url=url, data=json.dumps(data), headers=headers, verify=False)
    if resp.status_code != 201:
        raise Exception('Request for OpenSDS Token failed')

    return resp.headers['X-Subject-Token']


def get_url(project_id=None):
    if project_id is None:
        token = get_opensds_token(OPENSDS_IP, OPENSDS_USER, OPENSDS_PASS)
        project_id = get_project_id(OPENSDS_IP, OPENSDS_USER, token)

    return(
        "http://" + ORCHESTRATOR_IP +
        ":" + ORCHESTRATOR_PORT +
        "/v1beta/" + project_id +
        "/orchestration/")
