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

from orchestration.connectionmanager.OrchestrationConstants \
    import OrchConstants
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
        url = OrchConstants().get_st2_token_url(server)
        req = requests.post(url,
                            auth=HTTPBasicAuth(self.username, self.passwd),
                            verify=False)
        response = req.json()
        return response['token']

    # Fucntion to list the action
    # Caller can store the result in DB
    # @Input: ActionName
    # @output: the ActionDetails
    def listActions(self, packName=''):
        authToken = self.authenticate()
        headers = {'X-Auth-Token': authToken}
        url = OrchConstants().get_st2_action_list_url(self.server)
        req = requests.get(url, headers=headers, verify=False)
        response = req.json()
        for elem in response:
            if(elem['name'] != packName):
                continue
            else:
                return(elem)

    # Function to execute the Action
    # @Input: The post request should have the data as the 'action'
    # And any parameter that is required by the actions
    # @output: Result returned by the Stackstorm
    def executeAction(self, reqData):
        authToken = self.authenticate()
        url = OrchConstants().get_st2_executions_post_url(self.server)
        hdr = {'X-Auth-Token': authToken, 'Content-Type': 'application/json'}
        resp = requests.post(
                url, data=json.dumps(reqData), headers=hdr, verify=False)
        return(resp.text)

    def getExecutionStats(self, execId):
        authToken = self.authenticate()
        hdr = {'X-Auth-Token': authToken}
        url = OrchConstants().get_st2_executions_get_url(self.server) \
            + '/' + execId + '/output'
        resp = requests.get(url, headers=hdr, verify=False)
        return(resp.text)
