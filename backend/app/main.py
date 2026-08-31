from fastapi import FastAPI

from app.database import create_table
from app.api.v1.words import router as router_words
from app.api.v1.auth import router as router_auth

app = FastAPI(title="chnzme")

app.include_router(router_words, prefix="/api/v1", tags=["words"])
app.include_router(router_auth, prefix="/api/v1", tags=["auth"])

# VIDEO
# GET    /words/{word_id}/video
# POST   /words/{word_id}/video
# DELETE /words/{word_id}/video

create_table()
