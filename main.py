

import requests
import pytesseract
import cv2

from PIL import Image
from io import BytesIO

image_url = 'https://cdn.discordapp.com/attachments/846773201618468932/966671714064936960/unknown.png'


def image_data_from_url(img_url):
    r = requests.get(img_url)
    return Image.open(BytesIO(r.content))


def filter_text(search, text):
    text_lst = text.split('\n')
    for line in text_lst:
        if search in line:
            return line


def extract_text(img):
    # gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img)
    return text


if __name__ == '__main__':
    tesseract_path = r'C:\Users\matt\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    try:
        image_data = image_data_from_url(image_url)
        content = extract_text(image_data)
        code = filter_text('Claim Code', content)
        print(code)

    except KeyboardInterrupt as ex:
        print('Exiting... 0')
        exit(0)
