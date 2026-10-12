import random
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.models.user_words import UserWord
from app.services.srs.settings import (
    EASE_AGAIN,
    EASE_EASY,
    EASE_HARD,
    EASY_BONUS,
    EASY_INTERVAL,
    GRADUATING_INTERVAL,
    HARD_MULTIPLIER,
    LEARNING_STEPS,
    MAX_INTERVAL,
    MIN_EASE,
    MIN_INTERVAL,
    NEW_INTERVAL_PERCENT,
    RELEARNING_STEPS,
    ROLLOVER_HOUR,
)

RATINGS = ("again", "hard", "good", "easy")
DAY_IN_MINUTES = 24 * 60


@dataclass
class ScheduleResult:
    status: str
    learning_step: int
    repetitions: int
    interval: int
    ease_factor: float
    lapses: int
    next_review: datetime


def _round(value: float) -> int:
    return int(value + 0.5)


def _day_start(moment: datetime) -> datetime:
    shifted = moment - timedelta(hours=ROLLOVER_HOUR)
    midnight = shifted.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight + timedelta(hours=ROLLOVER_HOUR)


def _fuzz_range(days: int) -> tuple[int, int]:
    if days < 3:
        return days, days

    delta = (
        1.0
        + 0.15 * max(min(days, 7) - 2.5, 0)
        + 0.10 * max(min(days, 20) - 7, 0)
        + 0.05 * max(days - 20, 0)
    )
    return _round(days - delta), _round(days + delta)


def _fuzzed(days: int, minimum: int, fraction: float) -> int:
    low, high = _fuzz_range(days)
    low = max(low, minimum, MIN_INTERVAL)
    high = max(high, low)
    return min(low + int(fraction * (high - low + 1)), MAX_INTERVAL)


def _hard_delay(steps: list[int], step: int) -> float:
    current = steps[step]

    if step > 0:
        return current
    if len(steps) > 1:
        return (current + steps[1]) / 2
    return min(current * 1.5, current + DAY_IN_MINUTES)


def _to_review(word: UserWord, days: int, ease: float, now: datetime) -> ScheduleResult:
    return ScheduleResult(
        status="review",
        learning_step=0,
        repetitions=word.repetitions + 1,
        interval=days,
        ease_factor=ease,
        lapses=word.lapses,
        next_review=_day_start(now) + timedelta(days=days),
    )


def _schedule_steps(
    word: UserWord,
    rating: str,
    now: datetime,
    status: str,
    steps: list[int],
    good_days: int,
    easy_days: int,
) -> ScheduleResult:
    step = min(word.learning_step, len(steps) - 1)

    if rating == "easy":
        return _to_review(word, easy_days, word.ease_factor, now)

    if rating == "good":
        step += 1
        if step >= len(steps):
            return _to_review(word, good_days, word.ease_factor, now)
        delay = steps[step]
    elif rating == "hard":
        delay = _hard_delay(steps, step)
    else:  # again
        step = 0
        delay = steps[0]

    return ScheduleResult(
        status=status,
        learning_step=step,
        repetitions=word.repetitions,
        interval=word.interval,
        ease_factor=word.ease_factor,
        lapses=word.lapses,
        next_review=now + timedelta(minutes=delay),
    )


def _schedule_review(word: UserWord, rating: str, now: datetime) -> ScheduleResult:
    interval = word.interval
    ease = word.ease_factor

    if rating == "again":
        lapse_interval = max(MIN_INTERVAL, _round(interval * NEW_INTERVAL_PERCENT))

        return ScheduleResult(
            status="relearning",
            learning_step=0,
            repetitions=word.repetitions,
            interval=min(lapse_interval, MAX_INTERVAL),
            ease_factor=max(MIN_EASE, ease - EASE_AGAIN),
            lapses=word.lapses + 1,
            next_review=now + timedelta(minutes=RELEARNING_STEPS[0]),
        )

    days_late = (
        max(0, (_day_start(now) - word.next_review).days) if word.next_review else 0
    )
    fraction = random.Random(f"{word.id}:{word.repetitions}").random()

    hard = _fuzzed(
        _round((interval + days_late / 4) * HARD_MULTIPLIER), interval + 1, fraction
    )
    good = _fuzzed(_round((interval + days_late / 2) * ease), hard + 1, fraction)
    easy = _fuzzed(
        _round((interval + days_late) * ease * EASY_BONUS), good + 1, fraction
    )

    if rating == "hard":
        return _to_review(word, hard, max(MIN_EASE, ease - EASE_HARD), now)
    if rating == "good":
        return _to_review(word, good, ease, now)
    return _to_review(word, easy, ease + EASE_EASY, now)


def schedule_card(user_word: UserWord, rating: str, now: datetime) -> ScheduleResult:
    if rating not in RATINGS:
        raise ValueError("Invalid rating")

    status = user_word.status

    if status in ("new", "learning"):
        return _schedule_steps(
            user_word,
            rating,
            now,
            "learning",
            LEARNING_STEPS,
            good_days=GRADUATING_INTERVAL,
            easy_days=EASY_INTERVAL,
        )

    if status == "relearning":
        return _schedule_steps(
            user_word,
            rating,
            now,
            "relearning",
            RELEARNING_STEPS,
            good_days=user_word.interval,
            easy_days=user_word.interval + 1,
        )

    if status == "review":
        return _schedule_review(user_word, rating, now)

    raise ValueError(f"Unknown card status: {status}")


def preview_intervals(user_word: UserWord, now: datetime) -> dict[str, int]:
    previews = {}

    for rating in RATINGS:
        result = schedule_card(user_word, rating, now)

        if result.status == "review":
            previews[rating] = result.interval * DAY_IN_MINUTES
        else:
            minutes = (result.next_review - now).total_seconds() / 60
            previews[rating] = max(1, _round(minutes))

    return previews
