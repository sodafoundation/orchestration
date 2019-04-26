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


class OrchConstants:
    HTTPS_URL = 'https://'
    ST2_TOKEN_URL = '/auth/v1/tokens'
    ST2_ACTION_LIST_URL = '/api/v1/actions'
    ST2_EXECUTIONS_URL = '/api/v1/executions'

    def get_st2_token_url(self, server):
        return(self.HTTPS_URL + server + self.ST2_TOKEN_URL)

    def get_st2_action_list_url(self, server):
        return(self.HTTPS_URL + server + self.ST2_ACTION_LIST_URL)

    def get_st2_executions_post_url(self, server):
        return(self.HTTPS_URL + server + self.ST2_EXECUTIONS_URL)

    def get_st2_executions_get_url(self, server):
        return(self.HTTPS_URL + server + self.ST2_EXECUTIONS_URL)
