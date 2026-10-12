import { useEffect, useState } from "react";

import ru from "../locales/ru";
import en from "../locales/en";

import {
  reviewUserWord,
  getReviewSessionWords,
  type UserWord,
} from "../api/userWords";
import { formatInterval } from "../utils/formatInterval";
import "../styles/Review.css";

type ReviewProps = {
  language: string;
};

const RATINGS = ["again", "hard", "good", "easy"] as const;
type Rating = (typeof RATINGS)[number];

const LEARN_AHEAD_MS = 20 * 60 * 1000;

const isLearning = (word: UserWord) =>
  word.status === "learning" || word.status === "relearning";

const dueTime = (word: UserWord) => word.nextReview?.getTime() ?? 0;

/** Какое слово показывать следующим (порядок как в Anki). */
function pickNext(queue: UserWord[], now: number): UserWord | undefined {
  const learning = queue
    .filter(isLearning)
    .sort((a, b) => dueTime(a) - dueTime(b));

  const dueLearning = learning.find((word) => dueTime(word) <= now);
  if (dueLearning) return dueLearning;

  const reviewOrNew = queue.find((word) => !isLearning(word));
  return reviewOrNew ?? learning[0];
}

/** Остаётся ли слово в этой сессии после ответа. */
function staysInSession(word: UserWord, now: number): boolean {
  return isLearning(word) && dueTime(word) - now <= LEARN_AHEAD_MS;
}

function Review({ language }: ReviewProps) {
  const text = language === "ru" ? ru.review : en.review;

  const [queue, setQueue] = useState<UserWord[]>([]);
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [total, setTotal] = useState(0);

  const [isLoading, setIsLoading] = useState(true);
  const [isAnswerVisible, setIsAnswerVisible] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [error, setError] = useState<string | null>(null);
  const [reviewError, setReviewError] = useState<string | null>(null);

  const currentWord = queue.find((word) => word.userWordId === currentId);

  useEffect(() => {
    async function loadReviewSession() {
      try {
        setIsLoading(true);
        setError(null);
        setReviewError(null);
        setIsAnswerVisible(false);

        const sessionWords = await getReviewSessionWords(language);

        setQueue(sessionWords);
        setTotal(sessionWords.length);
        setCurrentId(pickNext(sessionWords, Date.now())?.userWordId ?? null);
      } catch (error) {
        console.error(error);
        setError(text.errorLoading);
      } finally {
        setIsLoading(false);
      }
    }

    loadReviewSession();
  }, [language]);

  const handleReview = async (rating: Rating) => {
    if (!currentWord || isSubmitting) {
      return;
    }

    try {
      setIsSubmitting(true);
      setReviewError(null);

      const updatedWord = await reviewUserWord(
        currentWord.word.id,
        rating,
        language,
      );

      const now = Date.now();
      const nextQueue = queue.filter(
        (word) => word.userWordId !== currentWord.userWordId,
      );

      if (staysInSession(updatedWord, now)) {
        nextQueue.push(updatedWord);
      }

      setQueue(nextQueue);
      setCurrentId(pickNext(nextQueue, now)?.userWordId ?? null);
      setIsAnswerVisible(false);
    } catch (error) {
      console.error(error);
      setReviewError(text.reviewError);
    } finally {
      setIsSubmitting(false);
    }
  };

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (!currentWord) {
        return;
      }

      if (!isAnswerVisible) {
        if (event.code === "Space" || event.key === "Enter") {
          event.preventDefault();
          setIsAnswerVisible(true);
        }
        return;
      }

      const index = Number(event.key) - 1;

      if (index >= 0 && index < RATINGS.length) {
        handleReview(RATINGS[index]);
      }
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [currentWord, isAnswerVisible, isSubmitting]);

  if (isLoading) {
    return (
      <section className="review-page">
        <h1>#review</h1>
        <p className="review-state">{text.loading}</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="review-page">
        <h1>#review</h1>
        <p className="review-state">{error}</p>
      </section>
    );
  }

  if (!currentWord) {
    return (
      <section className="review-page">
        <h1>#review</h1>
        <p className="review-state">{text.noWords}</p>
      </section>
    );
  }

  const done = total - queue.length;

  return (
    <section className="review-page">
      <h1>#review</h1>

      <div className="review-progress">
        <div className="review-progress-track">
          <div
            className="review-progress-fill"
            style={{ width: `${total ? (done / total) * 100 : 0}%` }}
          />
        </div>
        <span>
          {done} / {total}
        </span>
      </div>

      <div className="review-card">
        <div className="review-word">{currentWord.word.character}</div>

        <div
          className={`review-answer ${isAnswerVisible ? "" : "review-answer--hidden"}`}
        >
          <div className="review-pinyin">{currentWord.word.pinyin}</div>
          <div className="review-translation">
            {currentWord.word.translation}
          </div>
        </div>

        {!isAnswerVisible ? (
          <button
            type="button"
            className="review-show-answer"
            onClick={() => setIsAnswerVisible(true)}
          >
            {text.showAnswer}
          </button>
        ) : (
          <div className="review-actions">
            {RATINGS.map((rating, index) => (
              <button
                key={rating}
                type="button"
                className={`review-rate review-rate--${rating}`}
                onClick={() => handleReview(rating)}
                disabled={isSubmitting}
              >
                <span>{text[rating]}</span>
                {currentWord.intervals && (
                  <small className="review-rate-interval">
                    {formatInterval(currentWord.intervals[rating], language)}
                  </small>
                )}
                <kbd>{index + 1}</kbd>
              </button>
            ))}
          </div>
        )}
      </div>

      {reviewError && <p className="review-inline-error">{reviewError}</p>}
    </section>
  );
}

export default Review;
