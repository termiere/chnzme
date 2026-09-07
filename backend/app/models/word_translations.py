from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.words import Word


class WordTranslation(Base):
    __tablename__ = "word_translations"

    __table_args__ = (
        UniqueConstraint(
            "word_id",
            "language",
            "translation",
            name="unique_word_translation",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"))
    language: Mapped[str] = mapped_column(String(10))
    translation: Mapped[str] = mapped_column(String(255))

    word: Mapped["Word"] = relationship(back_populates="translations")
