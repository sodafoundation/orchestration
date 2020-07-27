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
Unit test for database API.
"""

import mock
from orchestration.db import api
from orchestration.db import models

# ------------------------Test for service definition-------------------------


@mock.patch('orchestration.db.api.session_scope')
def test_get_service_definition_with_None(mock_session):
    mock_session.return_value.__enter__.return_value. \
        query.return_value.filter.return_value = []
    result = api.get_service_definition(
        None, 'a9e54256-2b8b-47d9-8ca1-355db52d60f1')
    assert result is None


@mock.patch('orchestration.db.api.session_scope')
def test_list_service_definitions(mock_session):
    mock_session.return_value.__enter__.return_value.query.return_value = []
    result = api.list_service_definitions(None)
    assert len(result) == 0


@mock.patch('uuid.uuid4')
@mock.patch('orchestration.db.api.session_scope')
def test_create_service_definition(mock_session, mock_uuid):
    mock_uuid.return_value = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected = models.ServiceDefinition()
    expected.id = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected.name = 'SD1'
    actual = api.create_service_definition(
        None, dict(name='SD1'), dict(
            id='85a56708-a072-4525-9cc2-bb2f4e4a93e1', name='WD1'))
    mock_session.return_value.__enter__.return_value.add.assert_called_once()
    if len(actual) > 0:
        for key, value in actual.items():
            if hasattr(models.ServiceDefinition(), key):
                assert getattr(expected, key) == value


# ------------------------Test for Service------------------------------------
@mock.patch('uuid.uuid4')
@mock.patch('orchestration.db.api.session_scope')
def test_create_service(mock_session, mock_uuid):
    mock_uuid.return_value = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected = models.Service()
    expected.id = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected.name = 'volume provsioning'
    actual = api.create_service(None, dict(name='volume provsioning'))

    mock_session.return_value.__enter__.return_value.add.assert_called_once()
    if len(actual) > 0:
        for key, value in actual.items():
            if hasattr(models.Service, key):
                assert getattr(expected, key) == value


@mock.patch('orchestration.db.api.session_scope')
def test_get_service(mock_session):
    fake_service = models.Service()
    mock_session.return_value.__enter__.return_value. \
        query.return_value.filter.return_value.first.return_value = \
        fake_service
    result = api.get_service(None, 'a9e54256-2b8b-47d9-8ca1-355db52d60f1')
    assert result == fake_service.to_dict()


@mock.patch('orchestration.db.api.session_scope')
def test_get_service_with_None(mock_session):
    mock_session.return_value.__enter__.return_value. \
        query.return_value.filter.return_value = []
    result = api.get_service(None, 'a9e54256-2b8b-47d9-8ca1-355db52d60f1')
    assert result is None


@mock.patch('orchestration.db.api.session_scope')
def test_list_services(mock_session):
    mock_session.return_value.__enter__.return_value.query.return_value = []
    result = api.list_services(None)
    assert len(result) == 0


# ------------------------Test for task------------------------------------
@mock.patch('uuid.uuid4')
@mock.patch('orchestration.db.api.session_scope')
def test_create_task(mock_session, mock_uuid):
    mock_uuid.return_value = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected = models.Task()
    expected.id = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected.name = 'volume provsioning'
    actual = api.create_task(None, dict(name='volume provsioning'))

    mock_session.return_value.__enter__.return_value.add.assert_called_once()
    for key, value in actual.__dict__.items():
        if hasattr(models.Task, key):
            assert getattr(expected, key) == value


@mock.patch('orchestration.db.api.session_scope')
def test_get_task(mock_session):
    fake_task = models.Task()
    mock_session.return_value.__enter__.return_value. \
        query.return_value.filter.return_value.first.return_value = \
        fake_task
    result = api.get_task(None, 'a9e54256-2b8b-47d9-8ca1-355db52d60f1')
    assert result == fake_task


@mock.patch('orchestration.db.api.session_scope')
def test_get_task_with_None(mock_session):
    mock_session.return_value.__enter__.return_value. \
        query.return_value.filter.return_value = []
    result = api.get_task(None, 'a9e54256-2b8b-47d9-8ca1-355db52d60f1')
    assert result is None


@mock.patch('orchestration.db.api.session_scope')
def test_list_tasks(mock_session):
    mock_session.return_value.__enter__.return_value.query.return_value = []
    result = api.list_tasks(None)
    assert len(result) == 0


# Test for Workflow Definition
@mock.patch('uuid.uuid4')
@mock.patch('orchestration.db.api.session_scope')
def test_create_workflow_definition(mock_session, mock_uuid):
    mock_uuid.return_value = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected = models.WorkflowDefinition()
    expected.id = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected.name = 'volume provisioning workflow def'
    expected.wfe_type = 'St2'
    actual = api.create_workflow_definition(
        None, dict(name='volume provisioning workflow def', wfe_type='St2'))

    mock_session.return_value.__enter__.return_value.add.assert_called_once()
    item_list = ['id', 'name', 'wfe_type']
    if actual is not None:
        for key, value in api.get_query_res(
                actual, models.WorkflowDefinition).items():
            if key not in item_list:
                next
            if hasattr(models.WorkflowDefinition, key):
                assert getattr(expected, key) == value


@mock.patch('orchestration.db.api.session_scope')
def test_get_workflow_definition(mock_session):
    fake_wfd = models.WorkflowDefinition()
    mock_session.return_value.__enter__.return_value. \
        query.return_value.filter.return_value.first.return_value = \
        fake_wfd
    result = api.get_workflow_definition(
                None, '85a56708-a072-4525-9cc2-bb2f4e4a93e1', 'St2')
    assert result is not None


@mock.patch('orchestration.db.api.session_scope')
def test_list_workflow_definitions(mock_session):
    mock_session.return_value.__enter__.return_value.query.return_value = []
    result = api.list_workflow_definitions(None)
    assert len(result) == 0


def update_workflow_definition(mock_session):
    api.update_workflow_definitions()


def delete_workflow_definition(mock_session):
    api.delete_workflow_definitions()


# Test for Workflow
@mock.patch('uuid.uuid4')
@mock.patch('orchestration.db.api.session_scope')
def test_create_workflow(mock_session, mock_uuid):
    mock_uuid.return_value = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected = models.Workflow()
    expected.id = '85a56708-a072-4525-9cc2-bb2f4e4a93e1'
    expected.name = 'volume provisioning workflow'
    expected.workflow_source = 'opensds.provision_volume'
    actual = api.create_workflow(
        None, dict(
            name='volume provisioning workflow',
            workflow_source='opensds.provision_volume'))

    mock_session.return_value.__enter__.return_value.add.assert_called_once()
    if actual is not None:
        for key, value in api.get_query_res(actual, models.Workflow).items():
            if hasattr(models.Workflow, key):
                assert getattr(expected, key) == value


@mock.patch('orchestration.db.api.session_scope')
def test_get_workflow(mock_session):
    fake_wf = models.Workflow()
    mock_session.return_value.__enter__.return_value. \
        query.return_value.filter.return_value.first.return_value = \
        fake_wf
    result = api.get_workflow(None, 'a9e54256-2b8b-47d9-8ca1-355db52d60f1')
    assert result == fake_wf.to_dict()


@mock.patch('orchestration.db.api.session_scope')
def test_list_workflows(mock_session):
    mock_session.return_value.__enter__.return_value.query.return_value = []
    result = api.list_workflows(None)
    assert len(result) == 0
