from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from app.core.config import settings

engine = create_engine(url=settings.DATABASE_URL, echo=True)
session_factory = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def create_table() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
