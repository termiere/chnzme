from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="chnzme")

WORDS = [
    {
        "id": 1,
        "character": "你好",
        "pinyin": "ni3 hao3",
        "translate": "hello",
    },
]


class WordResponse(BaseModel):
    id: int
    character: str
    pinyin: str
    translate: str


class WordCreate(BaseModel):
    character: str
    pinyin: str
    translate: str


class WordUpdate(BaseModel):
    character: str | None = None
    pinyin: str | None = None
    translate: str | None = None


def find_word_or_404(word_id):
    for word in WORDS:
        if word["id"] == word_id:
            return word
    raise HTTPException(status_code=404, detail="слово не найдено")


# README
# GET    /readme
@app.get("/readme")
def home():
    return {"status": "ok"}


# WORDS
# GET    /words
@app.get("/words")
def get_all_words():
    return {"words": WORDS}


# POST   /words
@app.post("/words", response_model=WordResponse)
def create_word(new_word: WordCreate):
    for word in WORDS:
        if word["character"] == new_word.character:
            raise HTTPException(status_code=409, detail="Слово уже существует")

    res = {
        "id": len(WORDS) + 1,
        "character": new_word.character,
        "pinyin": new_word.pinyin,
        "translate": new_word.translate,
    }
    WORDS.append(res)
    return res


# GET    /words/{id}
@app.get("/words/{word_id}")
def get_word_by_id(word_id: int):
    res = find_word_or_404(word_id)
    return {"message": "success", "word": res}


# PATCH  /words/{id}
@app.patch("/words/{word_id}")
def patch_word_by_id(word_id: int, word: WordUpdate):
    res = find_word_or_404(word_id)
    res.update(word.model_dump(exclude_unset=True))
    return {"message": "Success updated", "word": res}


# DELETE /words/{word_id}
@app.delete("/words/{word_id}")
def delete_word_by_id(word_id: int):
    res = find_word_or_404(word_id)
    WORDS.remove(res)
    return {"message": "Success delete"}


# VIDEO
# GET    /words/{word_id}/video
# POST   /words/{word_id}/video
# DELETE /words/{word_id}/video
