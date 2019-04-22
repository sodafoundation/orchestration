import requests

from st2common.runners.base_action import Action


class DeleteAttachmentAction(Action):
    def run(self, ip="", port="", projectid="", attachmentid=""):
        url = "http://" + \
            ip + ":" + \
            port + "/v1beta/" + \
            projectid + "/block/attachments/" + \
            attachmentid
        r = requests.delete(url=url)
        print(r.status_code)
        r.raise_for_status()


if __name__ == '__main__':
    DeleteAttachmentAction()
