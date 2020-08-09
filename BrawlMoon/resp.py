import json


class BrawlResponse:
    def __init__(self, status, message):
        self.status = status
        self.message = message

    @property
    def json(self):
        return json.loads(self.message)