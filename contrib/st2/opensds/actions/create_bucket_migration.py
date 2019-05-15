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
import json

from st2common.runners.base_action import Action


class CreateMigrationPlanAction(Action):
    def run(self, url,
            osds_tenant_id,
            user_id,
            name,
            description,
            src_bucket_name,
            dest_bucket_name,
            remain_source,
            osds_token):
        data = {
            "tenantId": osds_tenant_id,
            "userId": user_id,
            "Description": description,
            "Name": name,
            "Type": "migration",
            "RemainSource": remain_source,
            "SourceConn": {
                "StorType": "opensds-obj",
                "BucketName": src_bucket_name
            },
            "DestConn": {
                "StorType": "opensds-obj",
                "BucketName": dest_bucket_name
            }
        }
        headers = {
                   'accept': 'application/json',
                   'content-type': 'application/json',
                   'x-auth-token': osds_token
                   }
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        resp = r.json()
        return resp["plan"]["id"]
