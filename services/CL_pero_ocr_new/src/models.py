from typing import Optional

from pydantic import BaseModel


class OCRResult(BaseModel):
    name: Optional[str] = None
    xml: str
    text: Optional[str] = None


class OCREngine(BaseModel):
    id: int
    name: Optional[str] = None
    folder: str  # Name of folder in "./engines/
    config_file: Optional[str] = 'config.ini'
    pass
