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

# Stackstorm Workflow manager specific implementation

from orchestration.connectionmanager.orchestrationconstants \
    import Orchconstants
import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


class St2():
    def __init__(self, server, user, passwd):
        self.server = server
        self.username = user
        self.passwd = passwd

    # Function to authenticate with Stackstorm. It will return X-Auth_token
    def authenticate(self):
        server = self.server
        url = Orchconstants().get_st2_token_url(server)
        req = requests.post(url,
                            auth=HTTPBasicAuth(self.username, self.passwd),
                            verify=False)
        response = req.json()
        return response['token']

    # Fucntion to list the action
    # Caller can store the result in DB
    # @Input: ActionName
    # @output: the ActionDetails
    def list_actions(self, pack_name=''):
        auth_token = self.authenticate()
        headers = {'X-Auth-Token': auth_token}
        url = Orchconstants().get_st2_action_list_url(self.server)
        req = requests.get(url, headers=headers, verify=False)
        req = req.json()
        action_dict = {}
        if pack_name == '':
            return req
        else:
            for elem in req:
                if elem['runner_type'] != 'mistral-v2':
                    continue
                if(elem['pack'] != pack_name):
                    continue
                else:
                    action_dict[elem['ref']] = elem
        return action_dict

    # Function to get the action
    # Caller can store the result in DB
    # @Input: PackName, ActionId
    # @output: the ActionDetails
    def get_action(self, id, pack_name=''):
        auth_token = self.authenticate()
        headers = {'X-Auth-Token': auth_token}
        url = Orchconstants().get_st2_action_list_url(self.server) + '/' + id
        response = requests.get(url, headers=headers, verify=False)
        return response.status_code, response.json()

    def create_action(self, req_data):
        auth_token = self.authenticate()
        url = Orchconstants().get_st2_action_list_url(self.server)
        hdr = {'X-Auth-Token': auth_token, 'Content-Type': 'application/json'}
        resp = requests.post(
                url, data=json.dumps(req_data), headers=hdr, verify=False)
        return(resp.status_code, resp.text)

    def update_action(self, id, req_data):
        auth_token = self.authenticate()
        url = Orchconstants().get_st2_action_list_url(self.server) + '/' + id
        hdr = {'X-Auth-Token': auth_token, 'Content-Type': 'application/json'}
        resp = requests.put(
                url, data=json.dumps(req_data), headers=hdr, verify=False)
        return(resp.status_code, resp.text)

    def delete_action(self, id, req_data):
        auth_token = self.authenticate()
        url = Orchconstants().get_st2_action_list_url(self.server) + '/' + id
        hdr = {'X-Auth-Token': auth_token, 'Content-Type': 'application/json'}
        resp = requests.delete(
                url, data=json.dumps(req_data), headers=hdr, verify=False)
        return(resp.status_code, resp.text)

    # Function to execute the Action
    # @Input: The post request should have the data as the 'action'
    # And any parameter that is required by the actions
    # @output: Result returned by the Stackstorm
    def execute_action(self, req_data):
        auth_token = self.authenticate()
        url = Orchconstants().get_st2_executions_post_url(self.server)
        hdr = {'X-Auth-Token': auth_token, 'Content-Type': 'application/json'}
        resp = requests.post(
                url, data=json.dumps(req_data), headers=hdr, verify=False)
        return(resp.status_code, resp.text)

    def get_execution_stats(self, exec_id):
        auth_token = self.authenticate()
        hdr = {'X-Auth-Token': auth_token}
        url = Orchconstants().get_st2_executions_get_url(self.server) \
            + '/' + exec_id
        resp = requests.get(url, headers=hdr, verify=False)
        return(resp.status_code, resp.text)

    def get_execution_output(self, exec_id):
        auth_token = self.authenticate()
        hdr = {'X-Auth-Token': auth_token}
        url = Orchconstants().get_st2_executions_get_url(self.server) \
            + '/' + exec_id + '/output'
        resp = requests.get(url, headers=hdr, verify=False)
        return(resp.status_code, resp.text)
