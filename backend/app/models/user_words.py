from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.words import Word


class UserWord(Base):
    __tablename__ = "user_words"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "word_id",
            name="unique_user_word",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="new")
    repetitions: Mapped[int] = mapped_column(default=0)
    interval: Mapped[int] = mapped_column(default=0)
    ease_factor: Mapped[float] = mapped_column(default=2.5)
    next_review: Mapped[datetime | None] = mapped_column(nullable=True)
    last_review: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="user_words")
    word: Mapped["Word"] = relationship(back_populates="user_words")
