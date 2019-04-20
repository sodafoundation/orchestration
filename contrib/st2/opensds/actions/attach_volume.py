import requests
import json

from st2common.runners.base_action import Action


class AttachVolumeAction(Action):

    def run(self, url="", vol=""):
        data = {"VolumeId": vol}
        headers = {'content-type': 'application/json'}
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(r.status_code)
        print(r.text)


if __name__ == '__main__':

    AttachVolumeAction()
