import configparser
import os

import cv2
import tensorflow as tf
from pero_ocr.document_ocr.layout import PageLayout
from pero_ocr.document_ocr.page_parser import PageParser

ROOT = os.path.join(os.path.dirname(__file__), '..')
CONFIG_PATH = os.path.join(ROOT, 'engines/2020-12-07_universal/config.ini')
FILENAME_IMAGE = os.path.join(ROOT, 'tests/test image.jpg')


def get_config(config_path):
    assert os.path.exists(config_path)
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def get_image(filename):
    assert os.path.exists(filename)

    img = cv2.imread(FILENAME_IMAGE)
    return img


def main():
    print(tf)

    name = os.path.split(FILENAME_IMAGE)[-1]
    img = get_image(FILENAME_IMAGE)

    config = get_config(CONFIG_PATH)

    config_dir = os.path.dirname(CONFIG_PATH)

    page_parser = PageParser(config,
                             config_dir
                             )

    page_layout = PageLayout(id=name,
                             page_size=img.shape[:2],
                             )

    page_layout = page_parser.process_page(img, page_layout)

    page_layout.to_pagexml_string()
    # page_layout.to_pagexml(filename_xml)

    return page_layout


if __name__ == '__main__':
    main()
