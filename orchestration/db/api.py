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
Data access module.
"""

import uuid
from contextlib import contextmanager
from orchestration.db import Session
from orchestration.db import models


# session_scope can be used cleanly in transaction,
# references the officel document of sqlalchemy.
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()


def list_sd_wfd_associations(context, **filters):
    with session_scope() as session:
        query = session.query(models.ServiceDefinition,
                              models.WorkflowDefinition) \
            .filter(models.DefinitionAssociation.service_definition_id
                    == models.ServiceDefinition.id,
                    models.DefinitionAssociation.workflow_definition_id
                    == models.WorkflowDefinition.id) \
            .order_by(models.DefinitionAssociation.workflow_definition_id)
    if not query:
        return []
    else:
        return query.all()


def get_sd_wfd_association(context=None, id=''):
    with session_scope() as session:
        if id == '':
            return list_sd_wfd_associations(None)
        else:
            query = session.query(models.ServiceDefinition,
                                  models.WorkflowDefinition) \
                .filter(models.DefinitionAssociation.service_definition_id
                        == models.ServiceDefinition.id,
                        models.DefinitionAssociation.workflow_definition_id
                        == models.WorkflowDefinition.id) \
                .filter(models.ServiceDefinition.id == id) \
                .order_by(models.DefinitionAssociation.workflow_definition_id)
    if not query:
        return None
    else:
        return query.all()


# -------------------------data access for service definition------------------
def create_service_definition(context, values, workflow_definitions):
    try:
        if not values.get('id'):
            values['id'] = str(uuid.uuid4())

        service_definition = models.ServiceDefinition()
        service_definition.update(values)
        for workflow_definition in workflow_definitions:
            service_definition.workflow_definitions.append(workflow_definition)

        with session_scope() as session:
            session.add(service_definition)
    except RuntimeError:
        return None

    return get_service_definition(context, id=values['id'])


def get_service_definition(context=None, id=''):
    with session_scope() as session:
        if id == '':
            query = session.query(models.ServiceDefinition)
        else:
            query = session.query(models.ServiceDefinition).filter(
                models.ServiceDefinition.id == id)
    if not query or query.first() is None:
        return None
    else:
        return query.first().to_dict()


def list_service_definitions(context, **filters):
    with session_scope() as session:
        query = session.query(models.ServiceDefinition)
    if not query:
        return []
    else:
        return get_query_res(query.all(), models.ServiceDefinition)


def update_service_definition(context, values):
    pass


# -------------------------data access for service ----------------------------
def create_service(context, values):
    service = models.Service()
    for key, value in values.items():
        if hasattr(service, key):
            setattr(service, key, value)

    if not service.id:
        service.id = uuid.uuid4()

    with session_scope() as session:
        session.add(service)
    return service


def get_service(context, id):
    with session_scope() as session:
        query = session.query(models.Service).filter(
            models.Service.id == id)
    return None if not query else query.first()


def list_services(context, **filters):
    with session_scope() as session:
        query = session.query(models.Service)
    return [] if not query else query.all()


def update_service(context, values):
    pass


def delete_service(context, id):
    with session_scope() as session:
        session.query(models.Service).filter(
            models.Service.id == id).delete()


def delete_service_definition(context, id):
    with session_scope() as session:
        session.query(models.ServiceDefinition).filter(
            models.ServiceDefinition.id == id).delete()


# ------------------------data access for workflow definition-----------------
def create_workflow_definition(context, values):
    try:
        workflow_definition = models.WorkflowDefinition()
        for key, value in values.items():
            if hasattr(workflow_definition, key):
                setattr(workflow_definition, key, value)

        if not workflow_definition.id:
            workflow_definition.id = str(uuid.uuid4())
        with session_scope() as session:
            session.add(workflow_definition)
    except RuntimeError:
        return None
    return workflow_definition


def get_workflow_definition(context, id, wfe_type):
    with session_scope() as session:
        if id == '':
            query = session.query(models.WorkflowDefinition)
        else:
            query = session.query(models.WorkflowDefinition)\
                .filter(models.WorkflowDefinition.definition_source == id)\
                .filter(models.WorkflowDefinition.wfe_type == wfe_type)
    return None if not query else query.first()


def list_workflow_definitions(context, **filters):
    with session_scope() as session:
        query = session.query(models.WorkflowDefinition)
    if not query:
        return []
    else:
        return get_query_res(query.all(), models.WorkflowDefinition)


def update_workflow_definition():
    pass


def delete_workflow_definition():
    pass


# ------------------------data access for workflow --------------------------
def create_workflow(context, values):
    workflow = models.Workflow()
    for key, value in values.items():
        if hasattr(workflow, key):
            setattr(workflow, key, value)

    if not workflow.id:
        workflow.id = uuid.uuid4()
    with session_scope() as session:
        session.add(workflow)
    return workflow


def get_workflow(context, id):
    with session_scope() as session:
        query = session.query(models.Workflow).filter(
            models.Workflow.id == id)
    return None if not query else query.first()


def list_workflows(context, **filters):
    with session_scope() as session:
        query = session.query(models.Workflow)
    return [] if not query else get_query_res(query.all(), models.Workflow)


def update_workflow():
    pass


def delete_workflow():
    pass


# ------------------------data access for task -------------------------------
def create_task(context, values):
    task = models.Task()
    for key, value in values.items():
        if hasattr(task, key):
            setattr(task, key, value)

    if not task.id:
        task.id = uuid.uuid4()

    with session_scope() as session:
        session.add(task)
    return task


def get_task(context, id):
    with session_scope() as session:
        query = session.query(models.Task).filter(models.Task.id == id)
    return None if not query else query.first()


def list_tasks(context, **filters):
    with session_scope() as session:
        query = session.query(models.Task)
    return [] if not query else query.all()


def update_task():
    pass


def delete_task():
    pass


# This fucntion takes the query result as obj
# and the tablename of the object.
# Returns the list of all the objects converted to dict
def get_query_res(obj, tablename):
    res_list = []
    for obj_elem in obj:
        row_hash = {}
        for c in tablename.__table__.columns.keys():
            row_hash[str(c)] = getattr(obj_elem, c)
        res_list.append(row_hash)
    return res_list
