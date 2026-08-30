from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    character: Mapped[str]
    pinyin: Mapped[str | None] = mapped_column(nullable=True)
    translate: Mapped[str | None] = mapped_column(nullable=True)
