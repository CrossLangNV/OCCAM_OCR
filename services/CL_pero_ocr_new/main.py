import os
import subprocess
import tempfile
import warnings
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

app = FastAPI()


class OCRResult(BaseModel):
    name: Optional[str] = None
    xml: str
    text: Optional[str] = None


@app.get("/",
         )
async def name(
):
    return {'msg': "OCR: PERO-OCR-new micro-service."}


@app.post("/ocr/",
          response_model=OCRResult
          )
async def ocr_image(
        image: UploadFile = File(...)
):
    """
    The model gets loaded with every call, by calling OCR as a user-scripts
    """
    filename = image.filename

    with tempfile.TemporaryDirectory() as dirpath:
        filename_image_tmp = os.path.join(dirpath, filename)
        with open(filename_image_tmp, 'wb') as f_image:
            f_image.write(await image.read())

        filename_xml = os.path.join(dirpath, 'page.xml')
        filename_txt = os.path.join(dirpath, 'page.txt')

        proc = subprocess.run(['python', '-m', 'userscripts.run_ocr',
                               '-f', filename_image_tmp,
                               '-x', filename_xml,
                               '-t', filename_txt
                               ])

        try:
            proc.check_returncode()
        except Exception as e:
            warnings.warn(f"Userscript might have failed.\n{e}", UserWarning)

        try:
            with open(filename_xml) as f:
                xml = f.read()

            with open(filename_txt) as f:
                text = f.read()
        except Exception as e:
            raise HTTPException(status_code=416, detail='Engine failed to generate outputs.\n'
                                                        'Please contact an administrator.')

    result = OCRResult(name=filename,
                       xml=xml,
                       text=text)

    return result