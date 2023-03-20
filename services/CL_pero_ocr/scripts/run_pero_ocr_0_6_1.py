import os
import configparser
import warnings

import cv2
import numpy as np
from pero_ocr.document_ocr.layout import PageLayout
from pero_ocr.document_ocr.page_parser import PageParser

from scripts.run_foo import get_args
from src.dump import get_page_layout_text

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../MEDIA/pero-printed_modern-public-2022-11-18", 'config.ini')
if not os.path.exists(CONFIG_PATH):
    warnings.warn("Config file not found: {}".format(CONFIG_PATH), ResourceWarning)

def main(filename: str,
         filename_xml: str,
         filename_txt: str,
         config_path: str=CONFIG_PATH):
    """
    Loosely based on https://github.com/DCGM/pero-ocr/blob/15df0ab73b8b2e3f9fb9d9b3009149f2abafe7fd/README.md
    filename: path to the input image file
    filename_xml: path to the output xml file
    filename_txt: path to the output txt file
    """

    # Read config file.
    config = configparser.ConfigParser()
    config.read(config_path)

    # Init the OCR pipeline.
    # You have to specify config_path to be able to use relative paths
    # inside the config file.
    page_parser = PageParser(config, config_path=os.path.dirname(config_path))

    # Read the document page image.
    image = cv2.imread(filename, 1)

    # Init empty page content.
    # This object will be updated by the ocr pipeline. id can be any string and it is used to identify the page.
    page_layout = PageLayout(id=filename,
                             page_size=(image.shape[0], image.shape[1]))

    # Process the image by the OCR pipeline
    page_layout = page_parser.process_page(image, page_layout)

    page_layout.to_pagexml(filename_xml)  # Save results as Page XML.
    text = get_page_layout_text(page_layout)
    with open(filename_txt, 'w', encoding='utf-8') as out_f:
        out_f.write(text)

    if 0:
        # Render detected text regions and text lines into the image and
        # save it into a file.
        rendered_image = page_layout.render_to_image(image)
        cv2.imwrite('page_image_render.jpg', rendered_image)

    if 0:
        # Save each cropped text line in a separate .jpg file.
        for region in page_layout.regions:
            for line in region.lines:
                cv2.imwrite(f'file_id-{line.id}.jpg', line.crop.astype(np.uint8))

    return {'xml': page_layout.to_pagexml_string(),
            'txt': text}

if __name__ == '__main__':
    args = get_args()

    filename = args.filename
    filename_xml = args.xml
    filename_txt = args.txt

    main(filename,
         filename_xml,
         filename_txt
         )
