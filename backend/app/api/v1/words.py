from fastapi import APIRouter

from app.services import words as words_service
from app.schemas import WordRequest

router = APIRouter()


@router.get("/words")
def get_all_words():
    return words_service.get_all_words()


@router.post("/words")
def create_word(new_word: WordRequest):
    return words_service.create_word(new_word)


@router.get("/words/{word_id}")
def get_word_by_id(word_id: int):
    return words_service.get_word_by_id(word_id)


@router.patch("/words/{word_id}")
def update_word_by_id(word_id: int, word: WordRequest):
    return words_service.update_word_by_id(word_id, word)


@router.delete("/words/{word_id}")
def delete_word_by_id(word_id: int):
    return words_service.delete_word_by_id(word_id)
