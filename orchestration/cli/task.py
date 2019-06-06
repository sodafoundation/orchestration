import requests
from utils import get_url

# API get tasks
def get_task(exec_id):
    url = get_url() + "tasks/" + exec_id
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for Instance list failed", resp.status_code)

    print(resp.text)

# API get workflows
def get_workflows():
    url = get_url() + "workflows"
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("Request for workflows list failed", resp.status_code)

    print(resp.text)
