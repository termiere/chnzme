from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.user_words import UserWord
from app.models.words import Word


def find_user_word(session: Session, user_id: int, word_id: int):
    stmt = select(UserWord).where(
        UserWord.user_id == user_id,
        UserWord.word_id == word_id,
    )

    return session.scalar(stmt)


def get_user_words(session: Session, user_id: int):
    stmt = (
        select(UserWord)
        .where(UserWord.user_id == user_id)
        .options(selectinload(UserWord.word).selectinload(Word.translations))
    )

    return session.scalars(stmt).all()


def get_review_words(session: Session, user_id: int, limit: int = 20):
    now = datetime.now()
    stmt = (
        select(UserWord)
        .where(UserWord.user_id == user_id, UserWord.next_review <= now)
        .options(selectinload(UserWord.word).selectinload(Word.translations))
        .order_by(UserWord.next_review)
        .limit(limit)
    )
    return session.scalars(stmt).all()


def get_learn_words(session: Session, user_id: int, limit: int = 20):
    stmt = (
        select(UserWord)
        .where(UserWord.user_id == user_id, UserWord.status == "new")
        .options(selectinload(UserWord.word).selectinload(Word.translations))
        .order_by(UserWord.id)
        .limit(limit)
    )
    return session.scalars(stmt).all()


def create_user_word(session: Session, user_id: int, word_id: int):
    user_word = UserWord(
        user_id=user_id,
        word_id=word_id,
    )

    session.add(user_word)
    session.commit()

    stmt = (
        select(UserWord)
        .where(UserWord.id == user_word.id)
        .options(selectinload(UserWord.word).selectinload(Word.translations))
    )

    return session.scalar(stmt)


def delete_user_word(session: Session, user_word: UserWord):
    session.delete(user_word)
    session.commit()


def get_user_words_stats(session: Session, user_id: int):
    now = datetime.now()

    learn_count = session.scalar(
        select(func.count())
        .select_from(UserWord)
        .where(UserWord.user_id == user_id, UserWord.status == "new")
    )

    review_count = session.scalar(
        select(func.count())
        .select_from(UserWord)
        .where(
            UserWord.user_id == user_id,
            UserWord.status != "new",
            UserWord.next_review <= now,
        )
    )

    return {
        "learn": learn_count or 0,
        "review": review_count or 0,
    }
