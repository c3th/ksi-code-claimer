

import pytesseract
import cv2

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from colorama import Fore, Back
from time import sleep, time
from os import path


class Frames:
    def __init__(self, config):
        self.started_at = config.started_at

        self.search_term = 'Claim Code:'
        self.output = './out'

        self.taken_codes = []
        self.frame_nr = 0
        self.loop = True

    def handle_code(self, code):
        with open('codes.txt', 'a') as f:
            f.write('{}\n'.format(code))

    def extract_frames(self, extracted_video):
        capture = cv2.VideoCapture(extracted_video)
        print('Extracting frames from video...')
        while self.loop:
            ms = round(time() * 1000)
            ping = round(((ms - self.started_at) / 1000) % 60)
            success, frame = capture.read()
            if success:
                code = self.extract_code(frame, ping)
                if code:
                    code = code.replace(self.search_term, '').strip()
                    if code not in self.taken_codes:
                        filter_code = code.split(' ')[0]
                        if len(filter_code) == 16 and filter_code not in self.taken_codes:
                            self.append_code(filter_code, ping)

    def append_code(self, code, ping):
        self.taken_codes.append(code)
        self.code_out(code, ping)
        self.handle_code(code)

    def split_video(self, video_path, new_path):
        loaded_video = self.load_video_info(video_path)
        frames = loaded_video.duration
        ffmpeg_extract_subclip(
            video_path, round(frames / 3), frames, targetname=new_path
        )
        return new_path

    def load_video(self, video_path):
        video = cv2.VideoCapture(video_path)
        return video

    def load_video_info(self, video_path):
        video = VideoFileClip(video_path)
        return video

    def filter_text(self, search, text):
        text_lst = text.split('\n')
        for line in text_lst:
            if search in line:
                return line

    def extract_text(self, img):
        text = pytesseract.image_to_string(img)
        return text

    def extract_code(self, frame, ms=time()):
        extracted_text = self.extract_text(frame)
        text_lst = extracted_text.split('\n')
        code = self.filter_text(self.search_term, extracted_text)
        output = '{}{}s{}'.format(Fore.LIGHTRED_EX, str(ms), Fore.RESET)
        found = '{}{}{}{} {}:{}{}'.format(
            Back.LIGHTBLACK_EX, Fore.WHITE, round(time()), Back.RESET,

            Fore.LIGHTBLACK_EX, len(text_lst) - 1, Fore.RESET
        )
        print(found, output, [i for i in text_lst if i])
        return code

    def write_out(self, frame, frame_output, ms):
        file_name = '{}/frame_{}.png'.format(
            frame_output, ms
        )
        cv2.imwrite(file_name, frame)
        return file_name

    def code_out(self, code, ms):
        output = '{}Since: {}s{}'.format(
            Fore.LIGHTBLUE_EX, str(ms), Fore.RESET)
        found = '{}{}{}{} {}{}{}'.format(
            Back.LIGHTGREEN_EX, Fore.WHITE, round(time()), Back.RESET,

            Fore.LIGHTGREEN_EX, code, Fore.RESET
        )
        # file_name = self.write_out(self.code_output, self.frame_nr, ms)
        print(found, output)
