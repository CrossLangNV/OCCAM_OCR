import os.path
import unittest

from scripts.run_foo import main as main_ocr
from scripts.run_pero_ocr_0_6_1 import main as main_ocr_0_6_1


class TestOCR(unittest.TestCase):

    def setUp(self) -> None:

        DIR = os.path.dirname(__file__)

        self.filename = os.path.join(DIR, 'test image.jpg')
        self.filename_xml = os.path.join(DIR, 'test.xml')
        self.filename_txt = os.path.join(DIR, 'test.txt')

    def test_ocr(self):
        results = main_ocr(self.filename,
                           self.filename_xml,
                           self.filename_txt)

        self.assertTrue(results)

        with self.subTest("xml"):
            self.assertTrue(results.get("xml"))

        with self.subTest("txt"):
            self.assertTrue(results.get("txt"))


class TestOCR2(unittest.TestCase):

    def setUp(self) -> None:

        DIR = os.path.dirname(__file__)

        self.filename = os.path.join(DIR, 'test image.jpg')
        self.filename_xml = os.path.join(DIR, 'test.xml')
        self.filename_txt = os.path.join(DIR, 'test.txt')

    def test_ocr(self):
        results = main_ocr_0_6_1(self.filename,
                           self.filename_xml,
                           self.filename_txt)

        self.assertTrue(results)

        with self.subTest("xml"):
            self.assertTrue(results.get("xml"))

        with self.subTest("txt"):
            self.assertTrue(results.get("txt"))
