from fastapi import FastAPI, UploadFile, File, HTTPException
from pero_ocr.document_ocr.layout import PageLayout
import traceback

from scripts.dump import get_image, get_engine, image_folder_name, layout_model_name, ocr_model_name, configuration_pero_ocr

app = FastAPI()

config = configuration_pero_ocr(image_folder_name, layout_model_name, ocr_model_name)
page_parser, engine_name, engine_version = get_engine(config=config, headers=None, engine_id=None)


@app.post("/ocr",
          # response_model=XMLTransOut
          )
async def ocr_image(
        image: UploadFile = File(...)
):
    filename = image.filename

    print('-- Load image --')
    contents = await image.read()
    img = get_image(contents)

    print('-- Process image --')
    # Process image
    try:
        page_layout = PageLayout(id=filename,
                                 page_size = img.shape[:2],
                                 )

        page_layout = page_parser.process_page(img, page_layout)

    except:
        exception = traceback.format_exc()
        raise HTTPException(status_code=420,
                            detail=exception
                            )

    xml = page_layout.to_pagexml_string()

    return xml
