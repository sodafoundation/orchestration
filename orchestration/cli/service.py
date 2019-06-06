import requests
import json
from utils import get_project_id, get_user_id, get_url


# API get service from id
def get_services(service_id):
    url = get_url() + "services/" + service_id
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Service failed", resp.status_code)

    print(resp.text)


# API get services
def list_services():
    url = get_url() + "services"
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Services list failed", resp.status_code)

    print(resp.text)


# API register services
def add_services():
    url = get_url() + "services"
    headers = {
        'content-type': 'application/json'
    }

    data = {
        "name": "volume provision",
        "description": "Volume Service",
        "tenant_id": get_project_id(),
        "user_id": get_user_id(),
        "input": "",
        "constraint": "",
        "group": "provisioning",
        "workflows": [
            {
                "definition_source": "opensds.provision-volume",
                "wfe_type": "st2"
            },
            {
                "definition_source": "opensds.snapshot-volume",
                "wfe_type": "st2"
            }

        ]

    }
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    if resp.status_code != 200:
        print("Request for Register Services failed", resp.status_code)

    print(resp.text)
