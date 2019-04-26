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

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from orchestration.utils.config import DATABASE
from orchestration.db.models import Base


# Declares global engine in here
__engine__ = None
# Declares global session in here
Session = None


def init_session():
    global __engine__, Session
    if not Session:
        __engine__ = engine_from_config(DATABASE)
        # autocommit is False by default in sessionmaker.
        Session = sessionmaker(bind=__engine__)


def init_db():
    Base.metadata.create_all(bind=__engine__)


def drop_db():
    Base.metadata.drop_all(bind=__engine__)
