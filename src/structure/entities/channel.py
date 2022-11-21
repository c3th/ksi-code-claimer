

from .video import *


class Channel:
    def __init__(self, channel_data):
        # print(channel_data['feed'])
        self.user = channel_data['feed']['title']
        self.id = channel_data['feed']['yt:channelId']
        self.uploads = []
        for entry in list(channel_data['feed']['entry']):
            self.uploads.append(Video(entry))
