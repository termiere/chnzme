from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.words import WordRequest, WordUpdateRequest
from app.repositories import words as words_repository


def find_word_or_404(session: Session, user_id: int, word_id: int):
    res = words_repository.find_word_by_id(session, user_id, word_id)
    if res is None:
        raise HTTPException(status_code=404, detail="слово не найдено")
    return res


def get_word_by_id(session: Session, user_id: int, word_id: int):
    return find_word_or_404(session, user_id, word_id)


def get_all_words(session: Session, user_id: int):
    return words_repository.get_all_words(session, user_id)


def create_word(session: Session, user_id: int, new_word: WordRequest):
    res = words_repository.find_word_by_character(session, user_id, new_word.character)
    if res is not None:
        raise HTTPException(status_code=409, detail="слово уже существует")

    return words_repository.create_word(
        session, user_id, new_word.character, new_word.pinyin, new_word.translate
    )


def update_word_by_id(
    session: Session, user_id: int, word_id: int, word: WordUpdateRequest
):
    find_word_or_404(session, user_id, word_id)
    return words_repository.update_word(
        session, user_id, word_id, word.character, word.pinyin, word.translate
    )


def delete_word_by_id(session: Session, user_id: int, word_id: int):
    find_word_or_404(session, user_id, word_id)
    return words_repository.delete_word(session, user_id, word_id)
