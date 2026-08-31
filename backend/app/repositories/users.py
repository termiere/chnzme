from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users import User


def find_user_by_username(session: Session, username: str):
    stmt = select(User).where(User.username == username)
    return session.scalar(stmt)


def find_user_by_id(session: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    return session.scalar(stmt)


def create_user(session: Session, username: str, password_hash: str):
    user = User(
        username=username,
        password_hash=password_hash,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
