from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.words import Word


def find_word_by_id(session: Session, word_id: int):
    return session.get(Word, word_id)


def find_word_by_character(session: Session, word_character: int):
    stmt = select(Word).where(Word.character == word_character)
    return session.scalar(stmt)


def get_all_words(session: Session):
    stmt = select(Word)
    return session.scalars(stmt).all()


def create_word(
    session: Session, word_character: str, word_pinyin: str, word_translate: str
):
    word = Word(
        character=word_character,
        pinyin=word_pinyin,
        translate=word_translate,
    )

    session.add(word)
    session.commit()
    session.refresh(word)

    return word


def update_word(
    session: Session,
    word_id: int,
    word_character: str,
    word_pinyin: str,
    word_translate: int,
):
    word = session.get(Word, word_id)

    word.character = word_character
    word.pinyin = word_pinyin
    word.translate = word_translate

    session.commit()
    return word


def delete_word(session: Session, word_id: int):
    word = session.get(Word, word_id)
    session.delete(word)
    session.commit()
    return True
