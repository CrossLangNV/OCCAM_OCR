from src.models import OCREngine

engines = [
    OCREngine(id=1,
              name='Complex printed and handwritten layout',
              folder='2020-12-07_universal'),
    OCREngine(id=2,
              name='Complex printed and handwritten layout (experimental)',
              folder='2021-06-08_universal'),
    OCREngine(id=3,
              name='Belgian Official Gazette',
              folder='BRIS_layout_finetuned_ocr'),
    OCREngine(id=4,
              name='Printed newspapers',
              folder='pero_eu_cz_print_newspapers_2020-10-07')
]
