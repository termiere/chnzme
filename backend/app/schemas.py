from pydantic import BaseModel


# модель для описания действий со словом
class WordRequest(BaseModel):
    character: str
    pinyin: str | None = None
    translate: str | None = None


class WordResponse(BaseModel):
    id: int
    character: str
    pinyin: str
    translate: str
