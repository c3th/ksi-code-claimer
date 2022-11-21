
from time import sleep, time
from colorama import init, Fore, Back
import cv2
import pytesseract

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")
ffmpeg_extract_subclip("ksi_full.mp4", 140, 200, targetname="cut.mp4")


init()


def filter_text(search, text):
    text_lst = text.split('\n')
    for line in text_lst:
        if search in line:
            return line


def extract_text(img):
    text = pytesseract.image_to_string(img)
    return text


def extract_code(ms):
    extracted_text = extract_text(frame)
    text_lst = extracted_text.split('\n')
    code = filter_text(search_term, extracted_text)
    output = '{}{}s{}'.format(Fore.LIGHTRED_EX, str(ms), Fore.RESET)
    found = '{}{}{}{} {}:{}{}'.format(
        Back.LIGHTBLACK_EX, Fore.WHITE, round(time()), Back.RESET,

        Fore.LIGHTBLACK_EX, len(text_lst) - 1, Fore.RESET
    )
    print(found, output, [i for i in text_lst if i])
    return code


def write_out(frame_output, frameNr, ms):
    file_name = '{}/frame_{}_{}.png'.format(frame_output,  frameNr, ms)
    cv2.imwrite(file_name, frame)
    return file_name


def code_out(code, ms):
    output = '{}Since: {}s{}'.format(Fore.LIGHTBLUE_EX, str(ms), Fore.RESET)
    found = '{}{}{}{} {}{}{}'.format(
        Back.LIGHTGREEN_EX, Fore.WHITE, round(time()), Back.RESET,

        Fore.LIGHTGREEN_EX, code, Fore.RESET
    )
    file_name = write_out(code_output, frameNr, ms)
    print(found, output, file_name)


if __name__ == "__main__":
    start_ms = round(time() * 1000)
    taken_codes = []
    search_term = 'Claim Code'
    video_capture = 'cut.mp4'
    frame_output = './out'
    code_output = './codes'

    capture = cv2.VideoCapture(video_capture)
    frameNr = 0

    try:
        while True:
            ms = round(time() * 1000)
            ping = round(((ms - start_ms) / 1000) % 60)
            success, frame = capture.read()

            if success:
                code = extract_code(ping)

                if code and code not in taken_codes:
                    print(code)
                    taken_codes.append(code)
                    code_out(code, ping)

            else:
                break

            frameNr += 1

        capture.release()
    except KeyboardInterrupt:
        print('Exiting... 0')
        exit(0)
