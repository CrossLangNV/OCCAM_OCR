import os

import cv2
import numpy as np


class Image:
    @classmethod
    def from_contents(cls, contents):
        """
        :param contents: file contents: file.read()

        :return:
        """
        nparr = np.fromstring(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return cls._post(img)

    @classmethod
    def from_path(cls, filename):
        assert os.path.exists(filename)  # CV2 will return None when path doesn't exist.
        img = cv2.imread(filename)
        return cls._post(img)

    @staticmethod
    def _post(img):
        if len(img.shape) == 2:
            img = np.stack([img, img, img], axis=2)
        return img
