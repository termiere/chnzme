from app.db import DATABASE


def find_word_by_id(word_id):
    for word in DATABASE:
        if word["word_id"] == word_id:
            return word
    return None


def find_word_by_character(word_character):
    for word in DATABASE:
        if word["character"] == word_character:
            return word
    return None


def get_all_words():
    return DATABASE


def create_word(word):
    res = {
        "word_id": len(DATABASE) + 1,
        "character": word.character,
        "pinyin": word.pinyin,
        "translate": word.translate,
    }
    DATABASE.append(res)
    return res


def update_word(res, word):
    res.update(word.model_dump(exclude_unset=True))
    return res


def delete_word(word):
    DATABASE.remove(word)
    return True
