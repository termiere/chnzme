from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_current_user, get_session
from app.models.users import User
from app.schemas.user_words import (
    ReviewRequest,
    UserWordResponse,
    UserWordsStatsResponse,
)
from app.services import user_words as user_words_service

router = APIRouter()


@router.get("/user-words", response_model=list[UserWordResponse])
def get_user_words(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_words_service.get_user_words(session, current_user.id)


@router.get("/user-words/learn", response_model=list[UserWordResponse])
def get_learn_words(
    limit: int = 20,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_words_service.get_learn_words(session, current_user.id, limit)


@router.get("/user-words/review", response_model=list[UserWordResponse])
def get_review_words(
    limit: int = 20,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_words_service.get_review_words(session, current_user.id, limit)


@router.get("/user-words/stats", response_model=UserWordsStatsResponse)
def get_user_words_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_words_service.get_user_words_stats(session, current_user.id)


@router.post("/user-words/{word_id}", response_model=UserWordResponse)
def add_word(
    word_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_words_service.add_word(session, current_user.id, word_id)


@router.post("/user-words/{word_id}/review", response_model=UserWordResponse)
def review_word(
    word_id: int,
    review: ReviewRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_words_service.review_word(
        session, current_user.id, word_id, review.rating
    )


@router.delete("/user-words/{word_id}")
def delete_word(
    word_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_words_service.delete_word(session, current_user.id, word_id)
