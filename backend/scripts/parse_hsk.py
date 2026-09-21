import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "hsk"


URLS = {
    1: "https://mandarinbean.com/new-hsk-1-word-list/",
    2: "https://mandarinbean.com/new-hsk-2-word-list/",
    3: "https://mandarinbean.com/new-hsk-3-word-list/",
}


def parse_hsk(level: int, url: str) -> None:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    words = []

    for row in soup.find_all("tr"):
        cells = row.find_all("td")

        if len(cells) < 5:
            continue

        character = cells[1].get_text(strip=True)
        pinyin = cells[2].get_text(strip=True)
        translation = cells[4].get_text(strip=True)

        if not character or not pinyin:
            continue

        words.append(
            {
                "character": character,
                "pinyin": pinyin,
                "translate": {"en": translation, "ru": ""},
                "hsk_level": level,
            }
        )

    output_path = DATA_DIR / f"hsk{level}.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(words, file, ensure_ascii=False, indent=2)

    print(f"HSK {level}: {len(words)} words")
    print(f"Saved to: {output_path}")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for level, url in URLS.items():
        parse_hsk(level, url)


if __name__ == "__main__":
    main()
