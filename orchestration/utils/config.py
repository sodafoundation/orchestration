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

import configparser
from cryptography.fernet import Fernet
import logging
from logging.handlers import RotatingFileHandler

# flask server configuration
HOST = "127.0.0.1"
PORT = "5000"
CONFIG_FILE = '/etc/opensds/orchestration.conf'

# logging configuration
LOGGING_FILE = "/var/log/opensds/orchestration.log"
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] [%(filename)s] " \
    "[%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] %(message)s"
LOGGING_LEVEL = "INFO"
logger = None
conf = None


def init_logging():
    global logger
    # Setting rotating files number to 5 and each will be of 1MB
    server_log_file = RotatingFileHandler(
                                            LOGGING_FILE,
                                            maxBytes=10000,
                                            backupCount=5
                                        )
    logger = logging.getLogger()
    '''
    Logging level is set to INFO
    It will log all log messages with INFO, WARNING, ERROR and CRITICAL
    To enable debug logging, change the INFO to DEBUG
    Levels hierarchy CRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET
    '''
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOGGING_FORMAT)
    server_log_file.setFormatter(formatter)

    logger.addHandler(server_log_file)


def init_config(file='orchestration.conf'):
    global conf
    global HOST
    global PORT

    conf = configparser.ConfigParser()
    dataset = conf.read(file)
    if len(dataset) == 0:
        logger.error("Failed to open orchestration config file: [%s]" % file)
        file = 'orchestration.conf'
        logger.warning("Creating default config file at: [%s]" % file)
        # create default template config file
        cfgfile = open(file, 'w')

        # fill config file with default data
        conf.add_section('orchestration')
        conf.set('orchestration', 'host', HOST)
        conf.set('orchestration', 'port', PORT)
        conf.add_section('workflow')
        conf.set('workflow', 'tech', 'St2')
        conf.set('workflow', 'host', '127.0.0.1')
        conf.set('workflow', 'username', 'St2')
        conf.set('workflow', 'encripted_password', 'false')
        conf.set('workflow', 'password', 'password')
        conf.set('workflow', 'phrase', '')

        conf.write(cfgfile)
        cfgfile.close()

    HOST = conf['orchestration']['host']
    PORT = conf['orchestration']['port']


def get_workflow_config():
    global conf
    tech = ''
    server = ''
    user = ''
    passwd = ''

    try:
        server = conf.get('workflow', 'host')
        user = conf.get('workflow', 'username')
        tech = conf.get('workflow', 'tech')
        encripted = conf.get('workflow', 'encripted_password')
        if encripted == 'false':
            passwd = conf.get('workflow', 'password')
        else:
            phrase = conf.get('workflow', 'phrase')
            ciphered_suite = Fernet(phrase.encode())
            passwd = (ciphered_suite.decrypt(passwd.encode()))
    except Exception as ex:
        print(passwd)
        print(ex)
        raise ex
    finally:
        return tech, server, user, passwd


init_logging()
init_config(CONFIG_FILE)

# database configuration
DATABASE = {
    'sqlalchemy.url': 'sqlite:///osdsorch.sqlite'
}
