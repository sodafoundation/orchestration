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

"""
Initialization of sqlalchemy ORM.
"""

#import logging
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from orchestration.utils.config import DATABASE
from orchestration.utils import config
from orchestration.db.models import Base


# Declares global engine in here
__engine__ = None
# Declares global session in here
Session = None
__engine__ = engine_from_config(DATABASE)
# autocommit is False by default in sessionmaker.
Session = sessionmaker(bind=__engine__)
Base.metadata.create_all(bind=__engine__)
session = Session()

# Logging initialized
#db_log_file = logging.FileHandler(config.DB_LOGGING_FILE, 'a')
#formatter = logging.Formatter(config.LOGGING_FORMAT)
#db_log_file.setFormatter(formatter)
#
#logger = logging.getLogger('db_logger')
#logger.setLevel(20)
#logger.addHandler(db_log_file)
#
def drop_db():
    Base.metadata.drop_all(bind=__engine__)


def create_defs():
    pass
