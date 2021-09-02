import asyncio
import os
import unittest

import requests

if 0:
    URL = 'http://localhost:9065/ocr'  # Local
else:
    URL = 'http://192.168.105.41:9065/ocr'  # GPU server
FILENAME_IMAGE = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
FILENAME_IMAGE2 = os.path.join(os.path.dirname(__file__), 'test_image_handwritten.jpg')


class TestAPI(unittest.TestCase):
    def test_ocr_post(self):

        with open(FILENAME_IMAGE, 'rb') as f:
            files = {'image': f}
            response = requests.post(URL,
                                     files=files)

        print(response.json())

        self._assert_response(response)

    def test_post_multiple_in_series(self):

        for filename_image in [FILENAME_IMAGE,
                               FILENAME_IMAGE2,
                               FILENAME_IMAGE
                               ]:
            with open(filename_image, 'rb') as f:
                files = {'image': f}
                response = requests.post(URL,
                                         files=files)

            with self.subTest(str(filename_image)):
                self._assert_response(response)

    def test_post_a_lot_in_series(self, n=10):
        i = 0
        for _ in range(n):
            for filename_image in [FILENAME_IMAGE,
                                   FILENAME_IMAGE2,

                                   ]:
                with open(filename_image, 'rb') as f:
                    files = {'image': f}
                    response = requests.post(URL,
                                             files=files)

                with self.subTest(f'Post {i}'):
                    self._assert_response(response)

                i += 1

    def test_post_in_parallel(self, n_loop=10):
        """
        While the API might be able to handle a single call. We should check if the API can handle multiple calls at once, mainly to check if the GPU memory can take it.

        :return:
        """

        filenames = [FILENAME_IMAGE,
                     FILENAME_IMAGE2]

        def func(self, i: int):
            filename = filenames[i % len(filenames)]

            with open(filename, 'rb') as f:
                files = {'image': f}
                response = requests.post(URL,
                                         files=files)

            self._assert_response(response, verbose=0)

            print(f'Finished async {i}')

        loop = asyncio.get_event_loop()

        for i in range(n_loop):
            loop.run_in_executor(None, func, self, i + 1)

        pass  # TODO
        # self.assertEqual(0, 1)

    def _assert_response(self, response, verbose=1):

        json = response.json()

        if verbose:
            print(response.json().get('text'))

        for key in ['name', 'xml', 'text']:
            self.assertIn(key, json.keys())
