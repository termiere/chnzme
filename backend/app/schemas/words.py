from pydantic import BaseModel


class TranslationRequest(BaseModel):
    language: str
    translation: str


class TranslationResponse(BaseModel):
    language: str
    translation: str

    model_config = {"from_attributes": True}


class WordRequest(BaseModel):
    character: str
    pinyin: str | None = None
    hsk_level: int
    translations: list[TranslationRequest]


class WordResponse(BaseModel):
    id: int
    character: str
    pinyin: str | None
    hsk_level: int
    translations: list[TranslationResponse]

    model_config = {"from_attributes": True}
