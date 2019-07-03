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
import xml.etree.ElementTree as ET

from st2common.runners.base_action import Action


class LoadObjsAction(Action):
    def run(self, url, backend_name, prefix, auth_token):
        body = """<?xml version='1.0' encoding='utf-8'?>
                 <LoadObjectsReq>
                    <Backend>{}</Backend>
                    <Prefix>{}</Prefix>
                 </LoadObjectsReq>""".format(backend_name, prefix)
        headers = {'content-type': 'application/xml',
                   'x-auth-token': auth_token,
                   'accept': 'application/xml'
                   }
        r = requests.put(url=url, data=body, headers=headers)
        print r.content
        r.raise_for_status()
        if r.status_code == requests.codes.ok:
            response = ET.fromstring(r.text)
            msg = response.find("Msg")
            print(msg)
