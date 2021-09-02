import argparse
import os

from pero_ocr.document_ocr.layout import PageLayout

from src.dump import get_image, configuration_pero_ocr, image_folder_name, layout_model_name, get_engine, \
    ocr_model_name, get_page_layout_text


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


def main():
    args = get_args()

    filename = args.filename
    filename_xml = args.xml
    filename_txt = args.txt

    with open(filename, 'rb') as f_image:
        img = get_image(f_image.read())

    id = os.path.split(filename)[-1]

    config = configuration_pero_ocr(image_folder_name, layout_model_name, ocr_model_name)
    page_parser, engine_name, engine_version = get_engine(config=config, headers=None, engine_id=None)

    page_layout = PageLayout(id=id,
                             page_size=img.shape[:2],
                             )

    page_layout = page_parser.process_page(img, page_layout)

    page_layout.to_pagexml(filename_xml)

    text = get_page_layout_text(page_layout)
    with open(filename_txt, 'w', encoding='utf-8') as out_f:
        out_f.write(text)

    return {'xml': page_layout.to_pagexml_string(),
            'txt': text}


if __name__ == '__main__':
    main()
