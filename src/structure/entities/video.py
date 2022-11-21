

class Video:
    def __init__(self, video_data):
        self.title = video_data['title']
        self.id = video_data['yt:videoId']
