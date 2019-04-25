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

import requests
from requests.auth import HTTPBasicAuth
import sys
from St2 import St2
import json

# This class is the interface for all the different form of 
# Workflow Manager
class Connector(object):

    # This function should read the Workflow Manager technology
    # from Database and based upon the technology, should 
    # return the instance of that technology
    def morph(self):
        # server = getServerName() #TODO
        # user = getUserName() # TODO
        # pass = getPass() # TODO

        tech = 'St2' # TODO: Read this tech from DB
        if tech == 'St2':
            return St2('100.64.40.190', 'st2admin', 'Ch@ngeMe')
