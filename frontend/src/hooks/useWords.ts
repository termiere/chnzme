import { useQuery } from "@tanstack/react-query";

import { getWords, type Word } from "../api/words";

export function useWords(hskLevel: number | null, language: string) {
  return useQuery<Word[], Error>({
    queryKey: ["words", hskLevel, language],
    queryFn: () => getWords(hskLevel!, language),
    enabled: hskLevel !== null,
  });
}
