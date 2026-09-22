import { useState } from "react";

import ru from "../locales/ru";
import en from "../locales/en";

import type { Word } from "../api/words";
import "../styles/Words.css";

interface WordListProps {
  words: Word[];
  userWordIds: Set<number>;
  isAuthenticated: boolean;
  onAddWord: (wordId: number) => Promise<void>;
  onLoginRequired: () => void;
  language: string;
}

export function WordList({
  words,
  userWordIds,
  isAuthenticated,
  onAddWord,
  onLoginRequired,
  language,
}: WordListProps) {
  const text = language === "ru" ? ru.words : en.words;

  const [addedWordIds, setAddedWordIds] = useState<Set<number>>(new Set());
  const [pendingWordId, setPendingWordId] = useState<number | null>(null);

  const handleAddClick = async (wordId: number) => {
    if (!isAuthenticated) {
      onLoginRequired();
      return;
    }

    setPendingWordId(wordId);
    setAddedWordIds((prev) => new Set(prev).add(wordId));

    try {
      await onAddWord(wordId);
    } catch (error) {
      console.error(`${text.addError} ${wordId}:`, error);

      setAddedWordIds((prev) => {
        const next = new Set(prev);
        next.delete(wordId);
        return next;
      });

      alert(text.addError);
    } finally {
      setPendingWordId(null);
    }
  };

  if (words.length === 0) {
    return <p className="words-empty">{text.noWords}</p>;
  }

  return (
    <div className="words-grid">
      {words.map((item) => {
        const isAdded = userWordIds.has(item.id) || addedWordIds.has(item.id);
        const isPending = pendingWordId === item.id;

        return (
          <div key={item.id} className="word-card">
            <div className="word-card-top">
              <span className="status-dot" />

              <button
                className={`word-add-btn ${isAdded ? "is-added" : ""}`}
                disabled={isAdded || isPending}
                onClick={() => handleAddClick(item.id)}
              >
                {isPending
                  ? text.saving
                  : isAdded
                    ? text.inDictionary
                    : `+ ${text.add}`}
              </button>
            </div>

            <div className="word-card-body">
              <span className="word-hanzi">{item.character}</span>
            </div>

            <div className="word-card-footer">
              <span className="word-pinyin">{item.pinyin}</span>
              <span className="word-divider">|</span>
              <span className="word-translation">{item.translation}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
