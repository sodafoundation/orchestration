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

from st2tests.base import BaseActionTestCase
from attach_volume import AttachVolumeAction
import mock


class AttachVolumeActionTestCase(BaseActionTestCase):
    action_cls = AttachVolumeAction

    def test_run(self):
        with mock.patch('requests.post') as mock_post:
            # Configure the mock to return a response
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {}

            action = self.get_action_instance()

            response = action.run(
                ip_addr="127.0.0.1",
                port="5000",
                tenant_id="123",
                volume_id="vol_name",
                host_info={
                    "host": "ubuntu",
                    "initiator": "iqn.1993-08.org.debian:01:437bac3717c8",
                    "ip": "100.64.41.133"
                    },
                access_protocol="iscsi",
                auth_token="12345")

            self.assertEqual(response, None)

            mock_post.assert_called_once_with(
                url='http://127.0.0.1:5000/v1beta/123/block/attachments',
                data=mock.ANY,  # JSON data to be handled externally
                headers={
                    'content-type': 'application/json',
                    'x-auth-token': '12345'}
            )
