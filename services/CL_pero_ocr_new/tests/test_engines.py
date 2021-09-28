import os
import unittest

from pero_ocr.document_ocr.layout import PageLayout
from pero_ocr.document_ocr.page_parser import PageParser

from src.engine_parser import get_config
from src.image_processing import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIR_ENGINES = os.path.join(ROOT, 'engines')
FILENAME_IMAGE = os.path.join(ROOT, 'tests/test image.jpg')


class TestEngines(unittest.TestCase):

    def setUp(self) -> None:
        self.name = os.path.split(FILENAME_IMAGE)[-1]
        self.img = Image.from_path(FILENAME_IMAGE)

    def test_from_dir(self):
        dir_names = [o for o in os.listdir(DIR_ENGINES)
                     if os.path.isdir(os.path.join(DIR_ENGINES, o))]
        for dir_name in dir_names:

            with self.subTest(dir_name):
                config_dir = os.path.join(DIR_ENGINES, dir_name)
                config = get_config(os.path.join(config_dir, 'config.ini'))

                page_parser = PageParser(config,
                                         config_dir
                                         )

                page_layout = PageLayout(id=self.name,
                                         page_size=self.img.shape[:2],
                                         )
                page_layout = page_parser.process_page(self.img, page_layout)

                xml = page_layout.to_pagexml_string()
                if 0:
                    print(xml)
                else:
                    print('# of chars in XML: ', len(xml))
                self.assertTrue(xml, 'Expected an output.')
