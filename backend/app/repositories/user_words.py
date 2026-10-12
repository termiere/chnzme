from datetime import datetime, timedelta
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.user_words import UserWord
from app.models.words import Word
from app.services.srs.settings import LEARN_AHEAD_MINUTES


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


def get_review_words(session: Session, user_id: int):
    now = datetime.now()
    stmt = (
        select(UserWord)
        .where(UserWord.user_id == user_id, UserWord.next_review <= now)
        .options(selectinload(UserWord.word).selectinload(Word.translations))
        .order_by(UserWord.next_review)
    )
    return session.scalars(stmt).all()


def update_review(session: Session, user_word: UserWord, result, now: datetime):
    user_word.status = result.status
    user_word.learning_step = result.learning_step
    user_word.repetitions = result.repetitions
    user_word.interval = result.interval
    user_word.ease_factor = result.ease_factor
    user_word.lapses = result.lapses
    user_word.next_review = result.next_review
    user_word.last_review = now

    session.commit()
    session.refresh(user_word)

    return user_word


def get_learn_words(session: Session, user_id: int):
    stmt = (
        select(UserWord)
        .where(UserWord.user_id == user_id, UserWord.status == "new")
        .options(selectinload(UserWord.word).selectinload(Word.translations))
        .order_by(UserWord.id)
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


def get_review_session_words(session: Session, user_id: int):
    now = datetime.now()
    learn_ahead = now + timedelta(minutes=LEARN_AHEAD_MINUTES)

    due_stmt = (
        select(UserWord)
        .where(
            UserWord.user_id == user_id,
            UserWord.status != "new",
            or_(
                UserWord.next_review <= now,
                and_(
                    UserWord.status.in_(("learning", "relearning")),
                    UserWord.next_review <= learn_ahead,
                ),
            ),
        )
        .options(selectinload(UserWord.word).selectinload(Word.translations))
        .order_by(UserWord.next_review)
    )

    due_words = session.scalars(due_stmt).all()

    new_stmt = (
        select(UserWord)
        .where(
            UserWord.user_id == user_id,
            UserWord.status == "new",
        )
        .options(selectinload(UserWord.word).selectinload(Word.translations))
        .order_by(UserWord.id)
    )

    new_words = session.scalars(new_stmt).all()

    return [*due_words, *new_words]
