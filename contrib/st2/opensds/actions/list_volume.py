import requests

from st2common.runners.base_action import Action


class ListVolumeAction(Action):
    def run(self, ip="", port="", projectid=""):
        url = "http://"+ip+":"+port+"/v1beta/"+projectid+"/block/volumes"
        r = requests.get(url=url)
        print(r.status_code)
        r.raise_for_status()
        print(r.text)


if __name__ == '__main__':
    ListVolumeAction()
