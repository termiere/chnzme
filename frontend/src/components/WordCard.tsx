// src/components/WordCard.tsx
import React from "react";
import type { Word } from "../api/words";
interface WordCardProps {
  word: Word;
}

export const WordCard: React.FC<WordCardProps> = ({ word }) => {
  return (
    <div className="word-card">
      <div className="word-chinese">{word.character}</div>
      <div className="word-pinyin">{word.pinyin}</div>
      <div className="word-translation">{word.translation}</div>
    </div>
  );
};
