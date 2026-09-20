import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import engine
from app.models.users import User
from app.models.words import Word
from app.models.user_words import UserWord
from app.models.word_translations import WordTranslation
from app.schemas.hsk import HSKWord

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "hsk" / "hsk1.json"


def seed_hsk() -> None:
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    words = [HSKWord.model_validate(word) for word in data]

    json_characters = {word.character for word in words}

    added_words = 0
    updated_words = 0
    deleted_words = 0
    added_translations = 0

    with Session(engine) as session:
        db_words = session.scalars(select(Word)).all()

        for word in db_words:
            if word.character not in json_characters:
                session.execute(delete(UserWord).where(UserWord.word_id == word.id))

                session.execute(
                    delete(WordTranslation).where(WordTranslation.word_id == word.id)
                )

                session.delete(word)
                deleted_words += 1

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

                else:
                    existing_translation.translation = translation

        session.commit()

    print(f"added_words: {added_words}")
    print(f"updated_words: {updated_words}")
    print(f"deleted_words: {deleted_words}")
    print(f"added_translations: {added_translations}")


if __name__ == "__main__":
    seed_hsk()
