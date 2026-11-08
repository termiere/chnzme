import type { WordDTO, Word } from "../api/words";

export interface UserWordResponseDTO {
  id: number;
  word: WordDTO;

  status: string;
  learning_step: number;
  repetitions: number;
  interval: number;
  ease_factor: number;
  lapses: number;
  next_review: string | null;
  last_review: string | null;
  intervals?: Record<string, number> | null;
}

export interface UserWord {
  userWordId: number;
  word: Word;

  status: string;
  learningStep: number;
  repetitions: number;
  interval: number;
  easeFactor: number;
  lapses: number;
  nextReview: Date | null;
  lastReview: Date | null;
  intervals: Record<string, number> | null;
}

export interface ReviewRequestDTO {
  rating: "again" | "hard" | "good" | "easy";
}

export interface UserWordsStatsDTO {
  learn: number;
  review: number;
}

export interface HskStatsDTO {
  added_words_count: number;
  total_words_count: number;
}
