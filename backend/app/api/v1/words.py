from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services import words as words_service
from app.schemas import WordRequest, WordResponse
from app.dependency import get_session

router = APIRouter()


@router.get("/words", response_model=list[WordResponse])
def get_all_words(session: Session = Depends(get_session)):
    return words_service.get_all_words(session)


@router.post("/words", response_model=WordResponse)
def create_word(new_word: WordRequest, session: Session = Depends(get_session)):
    return words_service.create_word(session, new_word)


@router.get("/words/{word_id}")
def get_word_by_id(word_id: int, session: Session = Depends(get_session)):
    return words_service.get_word_by_id(session, word_id)


@router.patch("/words/{word_id}")
def update_word_by_id(
    word_id: int, word: WordRequest, session: Session = Depends(get_session)
):
    return words_service.update_word_by_id(session, word_id, word)


@router.delete("/words/{word_id}")
def delete_word_by_id(word_id: int, session: Session = Depends(get_session)):
    return words_service.delete_word_by_id(session, word_id)
