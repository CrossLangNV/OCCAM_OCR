import argparse
import os

from pero_ocr.document_ocr.layout import PageLayout
from pero_ocr.document_ocr.page_parser import PageParser

from engines.available_engines import engines
from src.engine_parser import get_config
from src.image_processing import Image
from src.models import OCRResult

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIR_ENGINES = os.path.join(ROOT, 'engines')


def get_args():
    """
    method for parsing of arguments for PERO-OCR: OCR an image script
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--filename", help="Input filename to read the image.")
    parser.add_argument("-e", "--engine", help="Engine id to select the layout-analysis and OCR engine.")
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
    page_parser = get_page_parser(engine_id)

    # Processing
    page_layout = page_parser.process_page(img, page_layout)

    # Export parsing
    return export_page_layout(page_layout,
                              filename_xml,
                              filename_txt)


def get_page_parser(engine_id: int) -> PageParser:
    engine_id = int(engine_id)
    engine = next(filter(lambda e: e.id == engine_id, engines))

    config_dir = os.path.join(DIR_ENGINES, engine.folder)
    config = get_config(os.path.join(config_dir, engine.config_file))

    page_parser = PageParser(config,
                             config_dir
                             )

    return page_parser


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
    engine_id = args.engine

    main(filename,
         filename_xml,
         filename_txt,
         engine_id=engine_id
         )
