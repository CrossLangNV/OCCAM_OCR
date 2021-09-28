from typing import Optional

from pydantic import BaseModel


class OCRResult(BaseModel):
    name: Optional[str] = None
    xml: str
    text: Optional[str] = None


class OCREngine(BaseModel):
    pass
