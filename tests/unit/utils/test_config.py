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

from orchestration.utils import config


FILE = 'tests/unit/utils/orchestration_test.conf'


def test_config_init():
    config.init_config(FILE)
    assert config.HOST == '127.0.0.1'
    assert config.PORT == '5000'


def test_get_workflow_config():
    (tech, server, user, passwd) = config.get_workflow_config(FILE)
    assert tech == 'St2'
    assert server == '10.0.0.1'
    assert user == 'st2admin'
    assert passwd == '12345'
