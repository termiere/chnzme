from datetime import datetime

from app.models.user_words import UserWord
from app.services.srs.scheduler import schedule_card

NOW = datetime(2026, 9, 23, 12, 0, 0)


def make_user_word(
    status: str = "new",
    learning_step: int = 0,
    repetitions: int = 0,
    interval: int = 0,
    ease_factor: float = 2.5,
    lapses: int = 0,
) -> UserWord:
    return UserWord(
        status=status,
        learning_step=learning_step,
        repetitions=repetitions,
        interval=interval,
        ease_factor=ease_factor,
        lapses=lapses,
    )


def test_new_card_again():
    card = make_user_word()

    result = schedule_card(card, "again", NOW)

    assert result.status == "learning"
    assert result.learning_step == 0
    assert result.interval == 0
    assert result.next_review == datetime(2026, 9, 23, 12, 5)


def test_new_card_good():
    card = make_user_word()

    result = schedule_card(card, "good", NOW)

    assert result.status == "learning"
    assert result.learning_step == 1
    assert result.next_review == datetime(2026, 9, 23, 12, 10)


def test_learning_again_resets_step():
    card = make_user_word(status="learning", learning_step=2)

    result = schedule_card(card, "again", NOW)

    assert result.status == "learning"
    assert result.learning_step == 0
    assert result.next_review == datetime(2026, 9, 23, 12, 5)


def test_review_again_enters_relearning():
    card = make_user_word(status="review", interval=30, repetitions=5)

    result = schedule_card(card, "again", NOW)

    assert result.status == "relearning"
    assert result.learning_step == 0
    assert result.interval == 30
    assert result.lapses == 1
    assert result.next_review == datetime(2026, 9, 23, 12, 10)


def test_review_good_increases_interval():
    card = make_user_word(status="review", interval=10, ease_factor=2.5)

    result = schedule_card(card, "good", NOW)

    assert result.status == "review"
    assert result.interval == 25
    assert result.repetitions == 1


def test_review_easy_increases_interval_more():
    card = make_user_word(status="review", interval=10, ease_factor=2.5)

    result = schedule_card(card, "easy", NOW)

    assert result.status == "review"
    assert result.interval == 32
    assert result.repetitions == 1
    assert result.ease_factor == 2.65
