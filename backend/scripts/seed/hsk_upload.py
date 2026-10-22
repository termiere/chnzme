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

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "hsk"

DATA_PATHS = [
    DATA_DIR / "hsk1.json",
    DATA_DIR / "hsk2.json",
    DATA_DIR / "hsk3.json",
]


def seed_hsk() -> None:
    print("Читаю JSON...", flush=True)
    all_words = []

    for data_path in DATA_PATHS:
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        all_words.extend(HSKWord.model_validate(word) for word in data)

    json_words = {(word.character, word.hsk_level) for word in all_words}

    added_words = 0
    updated_words = 0
    deleted_words = 0
    added_translations = 0

    print(f"JSON загружен: {len(all_words)} слов", flush=True)
    print("Подключаюсь к базе...", flush=True)

    with Session(engine) as session:
        print("Подключение успешно", flush=True)
        db_words = session.scalars(select(Word)).all()

        for word in db_words:
            key = (word.character, word.hsk_level)

            if key not in json_words:
                session.execute(delete(UserWord).where(UserWord.word_id == word.id))

                session.execute(
                    delete(WordTranslation).where(WordTranslation.word_id == word.id)
                )

                session.delete(word)
                deleted_words += 1

        print("Начинаю обработку слов...", flush=True)
        for hsk_word in all_words:

            if added_words % 50 == 0:
                print(f"Обработка: {added_words} новых слов", flush=True)

            word = session.scalar(
                select(Word).where(
                    Word.character == hsk_word.character,
                    Word.pinyin == hsk_word.pinyin,
                    Word.hsk_level == hsk_word.hsk_level,
                )
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
                if word.pinyin != hsk_word.pinyin:
                    word.pinyin = hsk_word.pinyin
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
