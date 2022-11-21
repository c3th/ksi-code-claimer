

from .dispatcher import Dispatcher
from .requests import Request
from .frame import Frames
from .api import API

from colorama import init, Fore, Back
from time import time, sleep
init()


class Client:
    def __init__(self, config):
        self.track_channel = config['track_channel']

        self.started_at = round(time() * 1000)
        self.latest_upload = None
        self.loop = True
        self.pinged = 0

        self.requests = Request()
        self.frames = Frames(self)
        self.dispatch = Dispatcher(self)
        self.api = API(self)

        self.start()

    def get_channel_request(self):
        channel_data = self.api.get_channel(
            self.track_channel
        )
        return channel_data

    def start(self):
        try:
            try:
                while self.loop:
                    channel_update = self.get_channel_request()
                    latest_upload = channel_update.uploads[0]
                    if self.latest_upload == None:
                        self.latest_upload = latest_upload.id

                        # FOR DEV
                        # self.dispatch.listen(latest_upload)

                    if self.latest_upload != latest_upload.id:
                        self.latest_upload = latest_upload.id

                    sleep(1)
            except Exception as ex:
                print('client error', ex)
                exit(0)
        except KeyboardInterrupt:
            print('Exiting... 0')
            exit(0)
