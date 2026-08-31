from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.dependency import get_session, get_current_user
from app.services import auth as auth_service
from app.models.users import User

router = APIRouter()


@router.get("/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    return auth_service.create_user(session, user)


@router.post("/auth/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    session: Session = Depends(get_session),
):
    return auth_service.login(session, credentials)
