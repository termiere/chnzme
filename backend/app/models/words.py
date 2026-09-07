from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.user_words import UserWord
from app.models.word_translations import WordTranslation


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    character: Mapped[str] = mapped_column(String(50), unique=True)
    pinyin: Mapped[str | None] = mapped_column(String(100), nullable=True)
    hsk_level: Mapped[int]

    user_words: Mapped[list["UserWord"]] = relationship(back_populates="word")
    translations: Mapped[list["WordTranslation"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
