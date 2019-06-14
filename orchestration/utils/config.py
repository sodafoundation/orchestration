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
import errno
import os
from cryptography.fernet import Fernet
import logging
from logging.handlers import RotatingFileHandler

# flask server configuration
HOST = "127.0.0.1"
PORT = "5000"
config_file = 'orchestration.conf'


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


def init_config(file):
    global conf
    global HOST
    global PORT

    try:
        conf = configparser.ConfigParser()
        dataset = conf.read(file)
        if len(dataset) == 0:
            logger.error(
                "Failed to open orchestration config file: [%s]" % file)
            raise IOError(
                errno.ENOENT, os.strerror(errno.ENOENT), file)

        HOST = conf['orchestration']['host']
        PORT = conf['orchestration']['port']
    except Exception as ex:
        raise ex


def get_workflow_config(file):
    global conf
    tech = ''
    server = ''
    user = ''
    passwd = ''

    try:
        conf = configparser.ConfigParser()
        dataset = conf.read(file)
        if len(dataset) == 0:
            logger.error(
                "Failed to open orchestration config file: [%s]" % file)
            raise IOError(
                errno.ENOENT, os.strerror(errno.ENOENT), file)
        server = conf.get('workflow', 'host')
        user = conf.get('workflow', 'username')
        tech = conf.get('workflow', 'tech')
        encrypted = conf.get('workflow', 'encrypted_password')
        if encrypted == 'false':
            passwd = conf.get('workflow', 'password')
        else:
            phrase = conf.get('workflow', 'phrase')
            ciphered_suite = Fernet(phrase.encode())
            passwd = (ciphered_suite.decrypt(passwd.encode()))
    except Exception as ex:
        print(ex)
        raise ex

    return tech, server, user, passwd


init_logging()

# database configuration
DATABASE = {
    'sqlalchemy.url': 'sqlite:///osdsorch.sqlite'
}
