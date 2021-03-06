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

from st2common.runners.base_action import Action


class DeleteMigrationPlanAction(Action):
    def run(self, url,
            tenant_id,
            user_id,
            auth_token):
        headers = {
                   'accept': 'application/json',
                   'content-type': 'application/json',
                   'x-auth-token': auth_token
                   }
        r = requests.delete(url=url, headers=headers)
        r.raise_for_status()
