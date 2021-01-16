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
from create_volume import CreateVolumeAction
from nose.tools import assert_is_not_none
import mock


class CreateVolumeActionTestCase(BaseActionTestCase):
    action_cls = CreateVolumeAction

    def test_run(self):
        with mock.patch('requests.post') as mock_post:
            # Configure the mock to return a response
            mock_post.return_value.status_code = 200
            res = {"id": "12345"}
            mock_post.return_value.json.return_value = res

            action = self.get_action_instance()

            response = action.run(
                ip_addr="127.0.0.1", port="5000",
                tenant_id="123", name="vol_name", size=1, auth_token="12345")

            self.assertEqual(response, "12345")

            mock_post.assert_called_once_with(
                url='http://127.0.0.1:5000/v1beta/123/block/volumes',
                data=mock.ANY,  # JSON data to be handled externally
                headers={
                    'content-type': 'application/json',
                    'x-auth-token': '12345'}
            )
            # If the request is sent successfully,
            # then a response to be returned.
            assert_is_not_none(response)
