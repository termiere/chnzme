import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models.users import User
from app.models.words import Word
from app.models.user_words import UserWord
from app.models.word_translations import WordTranslation
from app.schemas.hsk import HSKWord

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "hsk" / "hsk1.json"


def seed_hsk() -> None:
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    words = [HSKWord.model_validate(word) for word in data]

    added_words = 0
    updated_words = 0
    added_translations = 0

    with Session(engine) as session:
        for hsk_word in words:
            word = session.scalar(
                select(Word).where(Word.character == hsk_word.character)
            )

            if word is None:
                word = Word(
                    character=hsk_word.character,
                    pinyin=hsk_word.pinyin,
                    hsk_level=hsk_word.hsk_level,
                )

                session.add(word)
                session.flush()

                added_words += 1

            else:
                word.pinyin = hsk_word.pinyin
                word.hsk_level = hsk_word.hsk_level
                updated_words += 1

            translations = {
                "en": hsk_word.translate.en,
                "ru": hsk_word.translate.ru,
            }

            for language, translation in translations.items():
                existing_translation = session.scalar(
                    select(WordTranslation).where(
                        WordTranslation.word_id == word.id,
                        WordTranslation.language == language,
                        WordTranslation.translation == translation,
                    )
                )

                if existing_translation is None:
                    session.add(
                        WordTranslation(
                            word_id=word.id,
                            language=language,
                            translation=translation,
                        )
                    )

                    added_translations += 1

        session.commit()

    print(f"Добавлено слов: {added_words}")
    print(f"Обновлено слов: {updated_words}")
    print(f"Добавлено переводов: {added_translations}")


if __name__ == "__main__":
    seed_hsk()
