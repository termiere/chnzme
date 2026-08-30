from fastapi import FastAPI

from app.api.v1.words import router as router_words
from app.database import create_table

app = FastAPI(title="chnzme")

app.include_router(router_words, prefix="/api/v1", tags=["words"])

# VIDEO
# GET    /words/{word_id}/video
# POST   /words/{word_id}/video
# DELETE /words/{word_id}/video

create_table()
