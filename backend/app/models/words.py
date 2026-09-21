from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.user_words import UserWord
from app.models.word_translations import WordTranslation


class Word(Base):
    __tablename__ = "words"

    __table_args__ = (
        UniqueConstraint(
            "character",
            "pinyin",
            "hsk_level",
            name="uq_words_character_pinyin_hsk_level",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    character: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    pinyin: Mapped[str | None] = mapped_column(String(100), nullable=False)
    hsk_level: Mapped[int] = mapped_column(Integer, nullable=False)

    user_words: Mapped[list["UserWord"]] = relationship(back_populates="word")
    translations: Mapped[list["WordTranslation"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
