from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services import words as words_service
from app.schemas.words import WordRequest, WordResponse
from app.dependency import get_session

router = APIRouter()


@router.get("/words", response_model=list[WordResponse])
def get_all_words(
    session: Session = Depends(get_session),
    hsk_level: int | None = Query(default=None, ge=1),
):
    return words_service.get_all_words(session, hsk_level)


@router.get("/words/{word_id}", response_model=WordResponse)
def get_word_by_id(word_id: int, session: Session = Depends(get_session)):
    return words_service.get_word_by_id(session, word_id)


@router.post("/words", response_model=WordResponse)
def create_word(new_word: WordRequest, session: Session = Depends(get_session)):
    return words_service.create_word(session, new_word)


@router.delete("/words/{word_id}")
def delete_word_by_id(word_id: int, session: Session = Depends(get_session)):
    return words_service.delete_word_by_id(session, word_id)
