

import xmltodict
import json

from .entities.channel import *


class API:
    def __init__(self, config):
        self.request = config.requests

    def filter_request(self, text):
        data_dict = xmltodict.parse(text)
        encoded_json = json.dumps(data_dict)
        decoded_json = json.loads(encoded_json)
        return decoded_json

    def get_channel(self, channel_id):
        r = self.request.get('/videos.xml?channel_id={}'.format(channel_id))
        json = self.filter_request(r.text)
        return Channel(json)
