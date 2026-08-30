from fastapi import HTTPException

from app.schemas import WordRequest
from app.repositories import words as words_repository


def find_word_or_404(word_id: int):
    res = words_repository.find_word_by_id(word_id)
    if res is None:
        raise HTTPException(status_code=404, detail="слово не найдено")
    return res


def get_word_by_id(word_id: int):
    return find_word_or_404(word_id)


def get_all_words():
    return words_repository.get_all_words()


def create_word(new_word: WordRequest):
    res = words_repository.find_word_by_character(new_word.character)
    if res is not None:
        raise HTTPException(status_code=409, detail="слово уже существует")

    return words_repository.create_word(
        new_word.character, new_word.pinyin, new_word.translate
    )


def update_word_by_id(word_id: int, word: WordRequest):
    get_word_by_id(word_id)
    return words_repository.update_word(
        word_id, word.character, word.pinyin, word.translate
    )


def delete_word_by_id(word_id: int):
    get_word_by_id(word_id)
    return words_repository.delete_word(word_id)
