from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import user_words as user_words_repository
from app.repositories import words as words_repository


def get_user_words(session: Session, user_id: int):
    return user_words_repository.get_user_words(session, user_id)


def add_word(session: Session, user_id: int, word_id: int):
    word = words_repository.find_word_by_id(session, word_id)
    if word is None:
        raise HTTPException(status_code=404, detail="слово не найдено")

    existing_user_word = user_words_repository.find_user_word(session, user_id, word_id)
    if existing_user_word is not None:
        raise HTTPException(status_code=409, detail="слово уже добавлено")
    return user_words_repository.create_user_word(session, user_id, word_id)


def delete_word(session: Session, user_id: int, word_id: int):
    user_word = user_words_repository.find_user_word(session, user_id, word_id)
    if user_word is None:
        raise HTTPException(status_code=404, detail="слово не найдено в вашем словаре")
    user_words_repository.delete_user_word(session, user_word)
    return {"message": "слово удалено"}


def review_word(session: Session, user_id: int, word_id: int, rating: str):
    user_word = user_words_repository.find_user_word(session, user_id, word_id)
    if user_word is None:
        raise HTTPException(status_code=404, detail="слово не найдено в вашем словаре")

    valid_ratings = {"again", "hard", "good", "easy"}
    if rating not in valid_ratings:
        raise HTTPException(status_code=400, detail="неверный рейтинг")

    now = datetime.now()

    if rating == "again":
        user_word.status = "learning"
        user_word.interval = 0
        user_word.next_review = now + timedelta(minutes=10)

    elif rating == "hard":
        user_word.status = "review"
        user_word.repetitions += 1

        if user_word.interval == 0:
            user_word.interval = 1
        else:
            user_word.interval = max(
                1,
                round(user_word.interval * 1.2),
            )

        user_word.next_review = now + timedelta(days=user_word.interval)

        user_word.ease_factor = max(
            1.3,
            user_word.ease_factor - 0.15,
        )

    elif rating == "good":
        user_word.status = "review"
        user_word.repetitions += 1

        if user_word.interval == 0:
            user_word.interval = 3
        else:
            user_word.interval = round(user_word.interval * user_word.ease_factor)

        user_word.next_review = now + timedelta(days=user_word.interval)

    elif rating == "easy":
        user_word.status = "review"
        user_word.repetitions += 1

        if user_word.interval == 0:
            user_word.interval = 7
        else:
            user_word.interval = round(user_word.interval * user_word.ease_factor * 1.3)

        user_word.next_review = now + timedelta(days=user_word.interval)

        user_word.ease_factor += 0.15

    user_word.last_review = now

    session.commit()
    session.refresh(user_word)

    return user_word


def get_review_words(session: Session, user_id: int, limit: int = 20):
    return user_words_repository.get_review_words(session, user_id, limit)


def get_learn_words(session: Session, user_id: int, limit: int = 20):
    return user_words_repository.get_learn_words(session, user_id, limit)


def get_user_words_stats(session: Session, user_id: int):
    return user_words_repository.get_user_words_stats(session, user_id)
