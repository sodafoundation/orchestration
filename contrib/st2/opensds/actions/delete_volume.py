import requests

from st2common.runners.base_action import Action


class DeleteVolumeAction(Action):
    def run(self, ip="", port="", projectid="", volumeid=""):
        url = "http://" + \
            ip + ":" + \
            port + "/v1beta/" + \
            projectid + "/block/volumes/" + \
            volumeid
        r = requests.delete(url=url)
        print(r.status_code)
        r.raise_for_status()


if __name__ == '__main__':
    DeleteVolumeAction()
