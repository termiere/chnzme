// src/api/userWords.ts
import type { WordDTO, Word } from "./words";
import { mapWordDtoToDomain } from "./words";

const API_URL = import.meta.env.VITE_API_URL;

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

export interface ReviewRequestDTO {
  rating: "again" | "hard" | "good" | "easy";
}

export interface UserWordsStatsDTO {
  learn: number;
  review: number;
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

export function mapUserWordDtoToDomain(
  dto: UserWordResponseDTO,
  lang: string = "ru",
): UserWord {
  return {
    userWordId: dto.id,
    word: mapWordDtoToDomain(dto.word, lang),

    status: dto.status,
    learningStep: dto.learning_step,
    repetitions: dto.repetitions,
    interval: dto.interval,
    easeFactor: dto.ease_factor,
    lapses: dto.lapses,
    nextReview: dto.next_review ? new Date(dto.next_review) : null,
    lastReview: dto.last_review ? new Date(dto.last_review) : null,
    intervals: dto.intervals ?? null,
  };
}

// --- API Service Methods ---

// Функция для получения токена (например, из localStorage)
function getAuthHeaders(): Record<string, string> {
  const token = localStorage.getItem("access_token"); // Или откуда вы берете JWT токен
  return {
    "Content-Type": "application/json",
    Accept: "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

// 1. Получение слов
export async function getUserWords(lang: string = "ru"): Promise<UserWord[]> {
  const response = await fetch(`${API_URL}/api/v1/user-words`, {
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error("Требуется авторизация");
    throw new Error("Failed to fetch user words");
  }

  const data: UserWordResponseDTO[] = await response.json();
  return data.map((dto) => mapUserWordDtoToDomain(dto, lang));
}

// 2. Добавление слова
export async function addUserWord(
  wordId: number,
  lang: string = "ru",
): Promise<UserWord> {
  const response = await fetch(`${API_URL}/api/v1/user-words/${wordId}`, {
    method: "POST",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error("Пользователь не авторизован");
    throw new Error("Failed to add word to user dictionary");
  }

  const data: UserWordResponseDTO = await response.json();
  return mapUserWordDtoToDomain(data, lang);
}

// 3. Отправка результата повторения (Review)
export async function reviewUserWord(
  wordId: number,
  rating: ReviewRequestDTO["rating"],
  lang: string = "ru",
): Promise<UserWord> {
  const response = await fetch(
    `${API_URL}/api/v1/user-words/${wordId}/review`,
    {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ rating }),
    },
  );

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Пользователь не авторизован");
    }

    throw new Error("Failed to submit review");
  }

  const data: UserWordResponseDTO = await response.json();
  return mapUserWordDtoToDomain(data, lang);
}

export async function getReviewSessionWords(
  lang: string = "ru",
  limit: number = 20,
): Promise<UserWord[]> {
  const response = await fetch(
    `${API_URL}/api/v1/user-words/review-session?limit=${limit}`,
    {
      headers: getAuthHeaders(),
    },
  );

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Authorization is required");
    }

    throw new Error("Failed to fetch review session");
  }

  const data: UserWordResponseDTO[] = await response.json();

  return data.map((dto) => mapUserWordDtoToDomain(dto, lang));
}

export async function getReviewWords(
  lang: string = "ru",
  limit: number = 20,
): Promise<UserWord[]> {
  const response = await fetch(
    `${API_URL}/api/v1/user-words/review?limit=${limit}`,
    {
      headers: getAuthHeaders(),
    },
  );

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Требуется авторизация");
    }

    throw new Error("Failed to fetch review words");
  }

  const data: UserWordResponseDTO[] = await response.json();

  return data.map((dto) => mapUserWordDtoToDomain(dto, lang));
}

export async function getLearnWords(
  lang: string = "ru",
  limit: number = 20,
): Promise<UserWord[]> {
  const response = await fetch(
    `${API_URL}/api/v1/user-words/learn?limit=${limit}`,
    {
      headers: getAuthHeaders(),
    },
  );

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Требуется авторизация");
    }

    throw new Error("Failed to fetch learn words");
  }

  const data: UserWordResponseDTO[] = await response.json();

  return data.map((dto) => mapUserWordDtoToDomain(dto, lang));
}

// 4. Удаление слова из изучении (Удаление связки по word_id)
export async function deleteUserWord(wordId: number): Promise<void> {
  const response = await fetch(`${API_URL}/api/v1/user-words/${wordId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Пользователь не авторизован");
    }

    throw new Error("Failed to delete word from user dictionary");
  }
}
