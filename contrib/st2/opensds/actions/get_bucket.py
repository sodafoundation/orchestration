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


class GetBucketAction(Action):
    def run(self, url, bucket_name, auth_token):
        headers = {
            'x-auth-token': auth_token
        }
        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        root = ET.fromstring(r.text)
        exists = False
        if root != '':
            ns = {'backend': 'http://s3.amazonaws.com/doc/2006-03-01'}
            for buckets in root.findall('backend:Buckets', ns):
                name = buckets.find('backend:Name', ns).text
                if name == bucket_name:
                    exists = True
                    create_date = buckets.find('backend:CreationDate',
                                               ns).text
                    backend = buckets.find('backend:LocationConstraint',
                                           ns).text
                    msg = "{name} was created on {date} for the {backend} " \
                          "backend storage"\
                          .format(name=bucket_name,
                                  date=create_date,
                                  backend=backend)
                    print(msg)

        if not exists:
            raise Exception('{} Not Found'.format(bucket_name))


if __name__ == '__main__':
    GetBucketAction()
