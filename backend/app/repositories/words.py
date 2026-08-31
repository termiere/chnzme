from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.words import Word


def find_word_by_id(session: Session, user_id: int, word_id: int):
    stmt = select(Word).where(Word.id == word_id, Word.user_id == user_id)
    return session.scalar(stmt)


def find_word_by_character(session: Session, user_id: int, word_character: str):
    stmt = select(Word).where(Word.character == word_character, Word.user_id == user_id)
    return session.scalar(stmt)


def get_all_words(session: Session, user_id: int):
    stmt = select(Word).where(Word.user_id == user_id)
    return session.scalars(stmt).all()


def create_word(
    session: Session,
    user_id: int,
    word_character: str,
    word_pinyin: str,
    word_translate: str,
):
    word = Word(
        character=word_character,
        pinyin=word_pinyin,
        translate=word_translate,
        user_id=user_id,
    )

    session.add(word)
    session.commit()
    session.refresh(word)

    return word


def update_word(
    session: Session,
    user_id: int,
    word_id: int,
    word_character: str | None,
    word_pinyin: str | None,
    word_translate: str | None,
):
    stmt = select(Word).where(Word.user_id == user_id, Word.id == word_id)
    word = session.scalar(stmt)
    if word is not None:

        if word_character is not None:
            word.character = word_character
        if word_pinyin is not None:
            word.pinyin = word_pinyin
        if word_translate is not None:
            word.translate = word_translate

        session.commit()

    session.refresh(word)
    return word


def delete_word(session: Session, user_id: int, word_id: int):
    stmt = select(Word).where(Word.user_id == user_id, Word.id == word_id)
    word = session.scalar(stmt)
    if word is not None:
        session.delete(word)
        session.commit()
        return True
    return False
