

import requests


class Request:
    def __init__(self):
        self.request = requests.Session()

        self.base_url = 'https://youtube.com/feeds'

    def get(self, endpoint):
        return self.request.get('{}{}'.format(self.base_url, endpoint))
