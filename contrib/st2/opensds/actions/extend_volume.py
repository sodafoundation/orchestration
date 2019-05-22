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


class ExtendVolumeAction(Action):
    def run(self, ip_addr, port, tenant_id,
            volume_id, size, auth_token):
        data = {
            "newSize": size
        }
        url = "http://" + \
              ip_addr + ":" + \
              port + "/v1beta/" + \
              tenant_id + "/block/volumes/" + \
              volume_id + "/resize"
        headers = {'content-type': 'application/json',
                   'x-auth-token': auth_token}
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        resp = r.json()

        status = resp["status"]
        while status != 'available':
            url = "http://" + \
                  ip_addr + ":" + \
                  port + "/v1beta/" + \
                  tenant_id + "/block/volumes/" + \
                  volume_id
            headers = {'x-auth-token': auth_token}
            r = requests.get(url=url, headers=headers)
            r.raise_for_status()
            resp = r.json()
            new_size = resp["size"]
            status = resp["status"]
        if new_size != size:
            raise Exception('Volume Extend Failed')
        msg = 'Volume capacity is extended to {}GB'.format(size)
        print(msg)
