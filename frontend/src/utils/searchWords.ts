const normalize = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim();

const compactPinyin = (s: string) => normalize(s).replace(/[\s'’\-\d]/g, "");

interface Searchable {
  character: string;
  pinyin: string | null;
  translation: string;
}

export function matchesWord(word: Searchable, query: string): boolean {
  const q = normalize(query);
  if (!q) return true;

  return (
    word.character.includes(query.trim()) ||
    normalize(word.translation).includes(q) ||
    compactPinyin(word.pinyin ?? "").includes(compactPinyin(query))
  );
}
