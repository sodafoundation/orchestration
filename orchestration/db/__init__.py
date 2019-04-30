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
from orchestration.db.models import Base, ServiceDefinition


# Declares global engine in here
__engine__ = None
# Declares global session in here
Session = None
__engine__ = engine_from_config(DATABASE)
# autocommit is False by default in sessionmaker.
Session = sessionmaker(bind=__engine__)
Base.metadata.create_all(bind=__engine__)
session = Session()
service_def = ServiceDefinition(
    name='migration_St2',
    description='Container for migration services'
    )
session.add(service_def)


def drop_db():
    Base.metadata.drop_all(bind=__engine__)


def create_defs():
    pass
#    service_def = {}
#    service_def['name'] = 'migration_st2'
#    service_def['description'] = 'Container for migration services'
#    create_service_definition(None, service_def)
