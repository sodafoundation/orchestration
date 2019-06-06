import requests
import json
from utils import OPENSDS_IP, OPENSDS_TOKEN, get_project_id, get_url

# API get instances
def get_instances():
    url = get_url() + "instances"
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Instance list failed", resp.status_code)

    print(resp.text)

# API run instance
def run_instance(ip, port, ):
    url = get_url() + "instances"
    headers = {
        'content-type': 'application/json'
    }

    data = {
        "action": "opensds.provision-volume",
        "parameters":
            {
                "ip_addr": OPENSDS_IP,
                "port": "50040",
                "tenant_id": get_project_id(),
                "size": 1,
                "name": "full",
                "auth_token": OPENSDS_TOKEN
            }
    }

    print(data)
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    if resp.status_code != 200:
        print("Request for Run Provision Volume Services failed", resp.status_code)

    print(resp.text)

