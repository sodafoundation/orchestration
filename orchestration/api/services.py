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

from orchestration.db.api \
    import create_workflow_definition, get_workflow_definition, \
    list_service_definitions, create_service_definition, \
    get_service_definition, list_sd_wfd_associations, get_sd_wfd_association
from orchestration.api.instances import get_wfd
from flask import Blueprint, jsonify, request
import json
from orchestration.api.apiconstants import Apiconstants
from orchestration.utils.config import logger

service = Blueprint("service", __name__)


# This API will provide the list of all the Service Definitions
# FIXME: temporarily changing the URL to:
# /orchestration/<string:tenant_id>/services
# Ideally it should be: /v1beta/<string:tenant_id>/orchestration/services
@service.route(
    "/orchestration/<string:tenant_id>/services",
    methods=['GET'])
def list_services(tenant_id=''):
    service_def_list = list_service_definitions(None)
    if not service_def_list:
        return jsonify([]), 200

    service_workflow_list = list_sd_wfd_associations(None)
    if not service_workflow_list:
        return jsonify([]), 200

    service_defs = []
    for service_def in service_def_list:
        wfs = []
        for sd, wd in service_workflow_list:
            if service_def['id'] == sd.id:
                wfd_hash = {'id': wd.id,
                            'name': wd.name,
                            'description': wd.description,
                            'definition': json.loads(wd.definition),
                            'definition_source': wd.definition_source,
                            'wfe_type': wd.wfe_type
                            }
                wfs.append(wfd_hash)
                service_def['workflows'] = wfs
                service_def['input'] = json.loads(wd.definition)
                service_defs.append(service_def)

    return jsonify(service_defs), 200


# This API will provide the details of the service 'id' provided
# FIXME: /orchestration/<string:tenant_id>/services/<string:service_id>
# It should be fixed to:
# /v1beta/<string:tenant_id>/orchestration/services/<string:service_id>
@service.route(
    "/orchestration/<string:tenant_id>/services/<string:service_id>",
    methods=['GET'])
def get_services(tenant_id='', service_id=''):
    service_def_hash = get_service_def(service_id)
    if not bool(service_def_hash):
        return jsonify({}), 404

    return jsonify(service_def_hash), 200


# API to register the ServiceDefinitions to Orchestration Manager
@service.route(
    "/orchestration/<string:tenant_id>/services",
    methods=['POST'])
def add_services(tenant_id=''):
    payload = request.get_json()
    service_data = json.loads(json.dumps(payload))
    service_data['tenant_id'] = tenant_id
    wf_def_sources = service_data['workflows']

    # Validate the request sent
    try:
        wf_def_sources = service_data['workflows']
    except Exception as e:
        err_msg = 'workflows param is missing'
        logger.error("%s: Exception [%s]", err_msg, str(e))
        return jsonify(err_msg), Apiconstants.HTTP_ERR_BAD_REQUEST
    try:
        if not service_data.get('group') \
            or not service_data.get('name') \
            or not service_data.get('user_id') \
           or not service_data.get('description'):
            logger.error("One of these: group/name/user_id is missing")
            logger.debug("request param is %s", service_data)
            raise ValueError('Value missing')
    except Exception as e:
        err_msg = 'One or more required value missing'
        logger.error("%s. Exception [%s]", err_msg, str(e))
        return jsonify(err_msg), Apiconstants.HTTP_ERR_BAD_REQUEST

    workflow_definitions = []

    if len(wf_def_sources) < 1 or not type(wf_def_sources) is list:
        err_msg = 'list of workflows not provided'
        logger.error("%s", err_msg)
        return jsonify(err_msg), Apiconstants.HTTP_ERR_BAD_REQUEST

    for wf_def_source in wf_def_sources:
        try:
            def_source_id = wf_def_source['definition_source']
            wfe_type = wf_def_source['wfe_type']
            if not def_source_id or not wfe_type:
                raise ValueError('WF Value missing')
        except Exception as e:
            err_msg = 'One or more required value of WF missing'
            logger.error("%s. Exception [%s]", err_msg, str(e))
            return jsonify(err_msg), Apiconstants.HTTP_ERR_BAD_REQUEST

        workflow_definition = get_wfd(def_source_id)
        if workflow_definition is None:
            continue
        if workflow_definition['runner_type'] == 'mistral-v2' and \
                workflow_definition['ref'] == def_source_id:
            wfd_hash = {'name': workflow_definition['name'],
                        'description': workflow_definition['description'],
                        'definition': json.dumps(
                            workflow_definition['parameters']),
                        'wfe_type': wfe_type,
                        'definition_source': workflow_definition['ref']
                        }
            # check if the entries are not present in DB then only
            # enter in DB
            wf_obj = get_workflow_definition(None, workflow_definition['ref'],
                                             wfe_type)
            if wf_obj is None:
                wf_obj = create_workflow_definition(None, wfd_hash)
        if wf_obj is not None:
            workflow_definitions.append(wf_obj)

    res = create_service_definition(None, service_data, workflow_definitions)

    return jsonify(res), 200


def get_service_def(service_id):
    service_def_hash = get_service_definition(None, service_id)
    if not bool(service_def_hash):
        return {}

    service_workflow_list = get_sd_wfd_association(None, service_id)
    if not service_workflow_list or service_workflow_list is None:
        return {}

    wfs = []
    for sd, wd in service_workflow_list:
        wfd_hash = {'id': wd.id,
                    'name': wd.name,
                    'description': wd.description,
                    'definition': json.loads(wd.definition),
                    'definition_source': wd.definition_source,
                    'wfe_type': wd.wfe_type
                    }
        wfs.append(wfd_hash)
        service_def_hash['workflows'] = wfs
        service_def_hash['input'] = json.loads(wd.definition)

    return service_def_hash
