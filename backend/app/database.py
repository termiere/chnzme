from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from app.core.quiet_dialect import get_engine

engine = get_engine()

session_factory = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass
