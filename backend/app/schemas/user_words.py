from typing import Literal
from datetime import datetime
from pydantic import BaseModel

from app.schemas.words import WordResponse


class UserWordResponse(BaseModel):
    id: int
    word: WordResponse

    status: str
    repetitions: int
    interval: int
    ease_factor: float
    next_review: datetime | None
    last_review: datetime | None

    model_config = {"from_attributes": True}


class ReviewRequest(BaseModel):
    rating: Literal["again", "hard", "good", "easy"]


class UserWordsStatsResponse(BaseModel):
    learn: int
    review: int
