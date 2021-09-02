import os
import unittest

import requests

if 0:
    URL = 'http://localhost:9065/ocr' # Local
else:
    URL = 'http://192.168.105.41:9065/ocr' # GPU server
FILENAME_IMAGE = os.path.join(os.path.dirname(__file__), 'test_image.jpg')


class TestAPI(unittest.TestCase):
    def test_ocr_post(self):

        with open(FILENAME_IMAGE,                   'rb') as f:
            files = {'image':f }
            response = requests.post(URL,
                          files=files)

        print(response.json())
        response
