from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import session_factory
from app.core.security import decode_access_token
from app.repositories import users as auth_repositories

security = HTTPBearer()


def get_session():
    with session_factory() as session:
        yield session


def get_current_user(
    session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        token = credentials.credentials
        user_id = decode_access_token(token)
    except:
        raise HTTPException(status_code=401, detail="неверный токен")

    user = auth_repositories.find_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="неверный токен")
    return user
