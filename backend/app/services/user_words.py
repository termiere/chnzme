from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import user_words as user_words_repository
from app.repositories import words as words_repository
from app.services.srs.scheduler import preview_intervals, schedule_card


def get_user_words(session: Session, user_id: int):
    return user_words_repository.get_user_words(session, user_id)


def add_word(session: Session, user_id: int, word_id: int):
    word = words_repository.find_word_by_id(session, word_id)
    if word is None:
        raise HTTPException(status_code=404, detail="The word was not found")

    existing_user_word = user_words_repository.find_user_word(session, user_id, word_id)
    if existing_user_word is not None:
        raise HTTPException(status_code=409, detail="The word has already been added")
    return user_words_repository.create_user_word(session, user_id, word_id)


def delete_word(session: Session, user_id: int, word_id: int):
    user_word = user_words_repository.find_user_word(session, user_id, word_id)
    if user_word is None:
        raise HTTPException(
            status_code=404, detail="The word was not found in your dictionary"
        )
    user_words_repository.delete_user_word(session, user_word)
    return {"message": "The word has been deleted"}


def review_word(session: Session, user_id: int, word_id: int, rating: str):
    user_word = user_words_repository.find_user_word(session, user_id, word_id)

    if user_word is None:
        raise HTTPException(
            status_code=404,
            detail="The word was not found in your dictionary",
        )

    valid_ratings = {"again", "hard", "good", "easy"}

    if rating not in valid_ratings:
        raise HTTPException(status_code=400, detail="Invalid rating")

    now = datetime.now()
    result = schedule_card(user_word, rating, now)

    updated_user_word = user_words_repository.update_review(
        session, user_word, result, now
    )
    updated_user_word.intervals = preview_intervals(updated_user_word, now)

    return updated_user_word


def get_review_words(session: Session, user_id: int):
    return user_words_repository.get_review_words(session, user_id)


def get_learn_words(session: Session, user_id: int):
    return user_words_repository.get_learn_words(session, user_id)


def get_review_session_words(session: Session, user_id: int):
    user_words = user_words_repository.get_review_session_words(session, user_id)
    now = datetime.now()

    for user_word in user_words:
        user_word.intervals = preview_intervals(user_word, now)

    return user_words


def get_user_words_stats(session: Session, user_id: int):
    return user_words_repository.get_user_words_stats(session, user_id)
