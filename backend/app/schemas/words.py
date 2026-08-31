from pydantic import BaseModel


class WordRequest(BaseModel):
    character: str
    pinyin: str
    translate: str


class WordUpdateRequest(BaseModel):
    character: str | None = None
    pinyin: str | None = None
    translate: str | None = None


class WordResponse(BaseModel):
    id: int
    character: str
    pinyin: str
    translate: str
