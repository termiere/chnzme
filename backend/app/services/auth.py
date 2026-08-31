from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import users as auth_repositories
from app.schemas.auth import UserCreate, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token


def create_user(session: Session, user: UserCreate):
    existing_user = auth_repositories.find_user_by_username(session, user.username)
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="пользователь уже существует")

    hashed_password = hash_password(user.password)
    return auth_repositories.create_user(session, user.username, hashed_password)


def login(session: Session, credentials: LoginRequest):
    existing_user = auth_repositories.find_user_by_username(
        session, credentials.username
    )
    if existing_user is None:
        raise HTTPException(status_code=401, detail="неверный username или пароль")

    correct_password = verify_password(
        credentials.password, existing_user.password_hash
    )
    if not correct_password:
        raise HTTPException(status_code=401, detail="неверный username или пароль")

    return {
        "access_token": create_access_token(existing_user.id),
        "token_type": "bearer",
    }
