// src/hooks/useWords.ts
import { useQuery } from "@tanstack/react-query";
import { getWords, type Word } from "../api/words";

export function useWords(hskLevel: number | null) {
  return useQuery<Word[], Error>({
    queryKey: ["words", hskLevel],
    queryFn: () => getWords(hskLevel!),
    enabled: hskLevel !== null,
  });
}
