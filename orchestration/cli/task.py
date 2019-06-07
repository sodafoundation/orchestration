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


import requests
from utils import get_url


# API get tasks
def get_task(exec_id):
    url = get_url() + "tasks/" + exec_id
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Instance list failed", resp.status_code)

    print(resp.text)


# API get workflows
def get_workflows():
    url = get_url() + "workflows"
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for workflows list failed", resp.status_code)

    print(resp.text)
