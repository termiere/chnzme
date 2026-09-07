from pydantic import BaseModel


class Translation(BaseModel):
    en: str
    ru: str


class HSKWord(BaseModel):
    character: str
    pinyin: str
    translate: Translation
    hsk_level: int
