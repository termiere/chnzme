import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users import User
from app.database import engine
from app.models.words import Word

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "hsk"

DATA_PATHS = sorted(DATA_DIR.glob("hsk*.json"))


def check_hsk() -> None:
    json_words = {}

    for data_path in DATA_PATHS:
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        hsk_level = int(data_path.stem.replace("hsk", ""))
        characters = {word["character"] for word in data}

        json_words[hsk_level] = characters

        print(f"{data_path.name}: {len(characters)} words")

    all_characters = {}

    for hsk_level, characters in json_words.items():
        for character in characters:
            all_characters.setdefault(character, []).append(hsk_level)

    duplicates = {
        character: levels
        for character, levels in all_characters.items()
        if len(levels) > 1
    }

    if duplicates:
        print("\nDuplicates:")
        for character, levels in duplicates.items():
            print(f"{character}: HSK {', '.join(map(str, levels))}")
    else:
        print("\nNo duplicates")

    with Session(engine) as session:
        db_words = session.scalars(select(Word)).all()

    db_by_level = {}

    for word in db_words:
        db_by_level.setdefault(word.hsk_level, set()).add(word.character)

    for hsk_level, json_characters in json_words.items():
        db_characters = db_by_level.get(hsk_level, set())

        missing = json_characters - db_characters
        extra = db_characters - json_characters

        print(f"\nHSK {hsk_level}")
        print(f"JSON: {len(json_characters)}")
        print(f"DB: {len(db_characters)}")

        if missing:
            print(f"Missing: {' '.join(sorted(missing))}")

        if extra:
            print(f"Extra: {' '.join(sorted(extra))}")

    all_json = set().union(*json_words.values())
    all_db = {word.character for word in db_words}

    if all_json == all_db:
        print("\nJSON and DB match")
    else:
        print("\nJSON and DB do not match")


if __name__ == "__main__":
    check_hsk()
