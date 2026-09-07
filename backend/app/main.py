from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.words import router as router_words
from app.api.v1.auth import router as router_auth
from app.api.v1.user_words import router as router_user_words

app = FastAPI(title="chnzme")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_words, prefix="/api/v1", tags=["words"])
app.include_router(router_auth, prefix="/api/v1", tags=["auth"])
app.include_router(router_user_words, prefix="/api/v1", tags=["user-words"])
