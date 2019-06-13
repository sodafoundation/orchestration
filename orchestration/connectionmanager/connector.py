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

from orchestration.connectionmanager.st2 import St2
from orchestration.utils.config import get_workflow_config
from orchestration.utils.config import config_file

# This class is the interface for all the different form of
# Workflow Manager


class Connector(object):

    # This function should read the Workflow Manager technology
    # from Database and based upon the technology, should
    # return the instance of that technology
    def morph(self):
        try:
            (tech, server, user, passwd) = get_workflow_config(config_file)
            if tech == 'St2':
                return St2(server, user, passwd)
        except Exception as ex:
            raise ex
