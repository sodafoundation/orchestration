import requests
import json

from st2common.runners.base_action import Action


class CreateVolumeAction(Action):

    def run(self, url="", name="", size=1):
        data = {
            "Name": name,
            "Description": "Test Volume from StackStorm",
            "Size": size
            }
        headers = {'content-type': 'application/json'}
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(r.status_code)
        print(r.text)
        resp = r.json()
        return resp["id"]


if __name__ == '__main__':

    volumeId = CreateVolumeAction()
    print('%s : %s' % 'Volume created with Id', volumeId)
