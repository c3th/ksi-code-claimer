

import requests

base_url = 'https://i.dreams.services'


class Dispatcher:
    def __init__(self, config):
        self.frames = config.frames

    def video_exist(self, file_path):
        try:
            with open(file_path):
                return True
        except FileNotFoundError:
            return False

    def download_video(self, video):
        try:
            # extracted_video_path = f'downloaded_{video.id}.mp4'
            extracted_video_path = f'edited.mp4'
            video_url = '{}/download?id={}'.format(base_url, video.id)
            video_path = video.title + '.mp4'
            if not self.video_exist(extracted_video_path):
                r = requests.get(video_url, stream=True)
                print('Found download for video...')
                with open(video_path, 'wb') as f:
                    print('Downloading video...')
                    for chunk in r.iter_content(chunk_size=255):
                        if chunk:
                            f.write(chunk)
                    f.close()

            # extracted_video = self.frames.split_video(
            #     video_path, extracted_video_path)

            self.frames.extract_frames(extracted_video_path)
        except Exception as ex:
            print('dispatcher error:', ex)

    def listen(self, video):
        print('Detecting an upload, downloading video...', video.title)
        self.download_video(video)
