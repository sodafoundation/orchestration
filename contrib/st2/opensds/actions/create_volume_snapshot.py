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

SNAPSHOT_STATUS_AVAILABLE = 'available'


class ExtendVolumeAction(Action):
    def run(self,
            host_ip,
            port,
            tenant_id,
            volume_id,
            name,
            description,
            profile_id,
            auth_token):
        data = {
            "name": name,
            "description": description,
            "volumeId": volume_id,
            "profileId": profile_id
        }
        url = "http://" + \
              host_ip + ":" + \
              port + "/v1beta/" + \
              tenant_id + "/block/snapshots/"
        headers = {'content-type': 'application/json',
                   'x-auth-token': auth_token}
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        resp = r.json()
        status = resp["status"]
        snapshot_id = resp["id"]
        while status != SNAPSHOT_STATUS_AVAILABLE:
            url = "http://" + \
                  host_ip + ":" + \
                  port + "/v1beta/" + \
                  tenant_id + "/block/snapshots/" + \
                  snapshot_id
            headers = {'x-auth-token': auth_token}
            r = requests.get(url=url, headers=headers)
            r.raise_for_status()
            resp = r.json()
            status = resp["status"]
        msg = 'Snapshot was created at ' + resp["createdAt"]
        print(msg)
