import configparser
import glob
import json
import os
import numpy as np
import cv2
from pero_ocr.document_ocr.page_parser import PageParser

ROOT = os.path.join(os.path.dirname(__file__), '..')


class settings:
    MEDIA_ROOT = os.path.join(ROOT, 'media')
    OUTPUT_DIR = os.path.join(ROOT, 'output_dir')

layout_model_name = 'test_layout_model'
ocr_model_name = 'test_ocr_model'
image_folder_name = '' # TODO?
# image_folder_name = os.path.join(ROOT, 'output_dir')

def get_image(contents):
    """

    :param contents: file contents: file.read()
    :return:
    """

    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if len(img.shape) == 2:
        img = np.stack([img, img, img], axis=2)

    return img


def get_engine(config, *args, **kwargs):
    # TODO

    page_parser = PageParser(config)

    return page_parser, None, None


def configuration_pero_ocr(image_folder_name, layout_model_name, ocr_model_name):
    # TODO Get from config.ini instead
    # 1) Configuration of PERO-OCR:

    config = configparser.ConfigParser()

    config['PAGE_PARSER'] = {'RUN_LAYOUT_PARSER': 'yes',
                             'RUN_LINE_CROPPER': 'yes',
                             'RUN_OCR': 'yes'
                             }

    config['PARSE_FOLDER'] = {'INPUT_IMAGE_PATH': os.path.join(settings.MEDIA_ROOT, image_folder_name),
                              'OUTPUT_XML_PATH': os.path.join(settings.OUTPUT_DIR, 'page'),
                              'OUTPUT_RENDER_PATH': os.path.join(settings.OUTPUT_DIR, 'render')
                              }

    # configuration of layout_model:
    layout_json_path = glob.glob(os.path.join(settings.MEDIA_ROOT, layout_model_name, "*.json"))

    try:
        layout_json_path = layout_json_path[0]
    except IndexError:
        print("ERROR: Layout model folder should contain a json configuration file.")
        raise

    with open(layout_json_path, "r") as json_file:
        layout_json = json.load(json_file)

    config['LAYOUT_PARSER'] = {'METHOD': layout_json['METHOD'],
                               'MODEL_PATH': os.path.join(settings.MEDIA_ROOT, layout_model_name, layout_json['NAME']),
                               'DOWNSAMPLE': str(layout_json['DOWNSAMPLE']),
                               'USE_CPU': layout_json['USE_CPU'],
                               'KEEP_LINES': layout_json['KEEP_LINES'],
                               'MIN_SIZE': str(layout_json['MIN_SIZE'])
                               }

    # configuration of line_cropper

    config['LINE_CROPPER'] = {'INTERP': '2',
                              'LINE_SCALE': '1',
                              'LINE_HEIGHT': '32'
                              }

    # configuration of ocr model:

    ocr_json_path = glob.glob(os.path.join(settings.MEDIA_ROOT, ocr_model_name, "*.json"))

    try:
        ocr_json_path = ocr_json_path[0]
    except IndexError:
        print("OCR model folder should contain a json configuration file.")
        raise

    config['OCR'] = {'OCR_JSON': ocr_json_path}

    return config


def get_page_layout_text(page_layout):
    text = ""
    for line in page_layout.lines_iterator():
        text += "{}\n".format(line.transcription)
    return text
