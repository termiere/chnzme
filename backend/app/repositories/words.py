from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.words import Word
from app.models.word_translations import WordTranslation


def find_word_by_id(session: Session, word_id: int):
    stmt = (
        select(Word).options(selectinload(Word.translations)).where(Word.id == word_id)
    )
    return session.scalar(stmt)


def find_word_by_character(session: Session, word_character: str):
    stmt = select(Word).where(Word.character == word_character)
    return session.scalar(stmt)


def get_all_words(session: Session, hsk_level: int | None = None):
    stmt = select(Word).options(selectinload(Word.translations))

    if hsk_level is not None:
        stmt = stmt.where(Word.hsk_level == hsk_level)

    return session.scalars(stmt).all()


def create_word(
    session: Session,
    word_character: str,
    word_pinyin: str | None,
    word_translations: list[dict[str, str]],
    hsk_level: int,
):
    word = Word(
        character=word_character,
        pinyin=word_pinyin,
        hsk_level=hsk_level,
    )

    for item in word_translations:
        translation = WordTranslation(
            language=item.language, translation=item.translation
        )

        word.translations.append(translation)

    session.add(word)
    session.commit()
    session.refresh(word)

    return word


def delete_word(session: Session, word_id: int):
    word = find_word_by_id(session, word_id)
    if word is None:
        return False

    session.delete(word)
    session.commit()

    return True
