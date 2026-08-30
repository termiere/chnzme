from sqlalchemy import select

from app.database import session_factory
from app.models.words import Word


def find_word_by_id(word_id: int):
    with session_factory() as session:
        return session.get(Word, word_id)


def find_word_by_character(word_character: int):
    with session_factory() as session:
        stmt = select(Word).where(Word.character == word_character)
        return session.scalar(stmt)


def get_all_words():
    with session_factory() as session:
        stmt = select(Word)
        return session.scalars(stmt).all()


def create_word(word_character: str, word_pinyin: str, word_translate: str):
    with session_factory() as session:
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
    word_id: int, word_character: str, word_pinyin: str, word_translate: int
):
    with session_factory() as session:
        word = session.get(Word, word_id)

        word.character = word_character
        word.pinyin = word_pinyin
        word.translate = word_translate

        session.commit()
        return word


def delete_word(word_id: int):
    with session_factory() as session:
        word = session.get(Word, word_id)
        session.delete(word)
        session.commit()
