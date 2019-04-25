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

from flask import Flask
from orchestration.api.services import service
from orchestration.api.instances import instance


class ServerManager:
    app = Flask(__name__)

    def __init__(self):
        self._init_logging()
        self._init_server()

    def _init_logging(self):
        pass

    def _init_server(self):
        self.app.url_map.strict_slashes = False

        # register router
        # self.app.register_blueprint(class_name)
        self.app.register_blueprint(service)
        self.app.register_blueprint(instance)

    def start(self):
        self.app.run("127.0.0.1", "8080")


server_manager = ServerManager()

if __name__ == '__main__':
    server_manager.start()
