from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.words import WordRequest
from app.repositories import words as words_repository


def find_word_or_404(session: Session, word_id: int):
    res = words_repository.find_word_by_id(session, word_id)
    if res is None:
        raise HTTPException(status_code=404, detail="слово не найдено")
    return res


def get_word_by_id(session: Session, word_id: int):
    return find_word_or_404(session, word_id)


def get_all_words(session: Session, hsk_level: int | None = None):
    return words_repository.get_all_words(session, hsk_level)


def create_word(session: Session, new_word: WordRequest):
    res = words_repository.find_word_by_character(session, new_word.character)
    if res is not None:
        raise HTTPException(status_code=409, detail="слово уже существует")

    return words_repository.create_word(
        session,
        new_word.character,
        new_word.pinyin,
        new_word.translations,
        new_word.hsk_level,
    )


def delete_word_by_id(session: Session, word_id: int):
    find_word_or_404(session, word_id)
    return words_repository.delete_word(session, word_id)
