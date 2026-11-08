import { mapWordDtoToDomain } from "./words";
import type {
  HskStatsDTO,
  ReviewRequestDTO,
  UserWord,
  UserWordResponseDTO,
} from "../types/userWords";

const API_URL = import.meta.env.VITE_API_URL;

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

function getAuthHeaders(): Record<string, string> {
  const token = localStorage.getItem("access_token");
  return {
    "Content-Type": "application/json",
    Accept: "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

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

export async function getAddedWordsByHSK(
  hskLevel: number,
): Promise<HskStatsDTO> {
  const response = await fetch(
    `${API_URL}/api/v1/user-words/stats/hsk/${hskLevel}`,
    {
      headers: getAuthHeaders(),
    },
  );

  if (!response.ok) {
    throw new Error(`Failed to load HSK stats: ${response.status}`);
  }

  return response.json();
}
