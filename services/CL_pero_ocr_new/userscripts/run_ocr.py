import argparse
import os

from pero_ocr.document_ocr.layout import PageLayout
from pero_ocr.document_ocr.page_parser import PageParser

from src.engine_parser import get_config
from src.image_processing import Image
from src.models import OCRResult


# from configs.parser import configuration_pero_ocr
# from src.dump import get_image, image_folder_name, layout_model_name, get_engine, \
#     ocr_model_name, get_page_layout_text


def get_args():
    """
    method for parsing of arguments for PERO-OCR: OCR an image script
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--filename", help="Input filename to read the image.")
    parser.add_argument("-x", "--xml", help="Output filename to save the xml to.")
    parser.add_argument("-t", "--txt", help="Output filename to save the text to.")

    args = parser.parse_args()

    return args


def main(filename,
         filename_xml,
         filename_txt,
         engine_id=1) -> OCRResult:
    # Image
    img = Image.from_path(filename)
    # Page layout init
    page_layout = PageLayout(id=os.path.split(filename)[-1],  # a name
                             page_size=img.shape[:2],
                             )

    # Get config/page_parser
    # TODO get config based on some ID
    engine_name = '2021-06-08_universal'
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    DIR_ENGINES = os.path.join(ROOT, 'engines')
    config_dir = os.path.join(DIR_ENGINES, engine_name)
    config = get_config(os.path.join(config_dir, 'config.ini'))

    page_parser = PageParser(config,
                             config_dir
                             )

    # Processing
    page_layout = page_parser.process_page(img, page_layout)

    # Export parsing
    return export_page_layout(page_layout,
                              filename_xml,
                              filename_txt)


def export_page_layout(page_layout: PageLayout,
                       filename_xml: str,
                       filename_txt: str,
                       ) -> OCRResult:
    text = get_page_layout_text(page_layout)

    page_layout.to_pagexml(filename_xml)

    with open(filename_txt, 'w', encoding='utf-8') as out_f:
        out_f.write(text)

    return OCRResult(xml=page_layout.to_pagexml_string(),
                     text=text,
                     name=page_layout.id)


def get_page_layout_text(page_layout: PageLayout) -> str:
    """

    :param page_layout: After running the OCR
    :return: Text saved as string with each line separeted by a \n.
    """

    text = ""
    for line in page_layout.lines_iterator():
        text += "{}\n".format(line.transcription)
    return text


if __name__ == '__main__':
    args = get_args()

    filename = args.filename
    filename_xml = args.xml
    filename_txt = args.txt

    main(filename,
         filename_xml,
         filename_txt
         )
