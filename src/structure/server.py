

import requests


class Server:
    def __init__(self):
        self.base_url = ''

        self.request = requests.Session()
