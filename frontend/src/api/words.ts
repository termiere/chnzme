const API_URL = import.meta.env.VITE_API_URL;

export interface TranslationDTO {
  language: string;
  translation: string;
}

export interface WordDTO {
  id: number;
  character: string;
  pinyin: string;
  hsk_level: number;
  translations: TranslationDTO[];
}

export interface Word {
  id: number;
  character: string;
  pinyin: string;
  hskLevel: number;
  translation: string;
}

export function mapWordDtoToDomain(dto: WordDTO, lang: string): Word {
  const matchedTranslation = dto.translations.find((t) => t.language === lang);
  const fallbackTranslation = dto.translations[0]?.translation ?? "";

  return {
    id: dto.id,
    character: dto.character,
    pinyin: dto.pinyin,
    hskLevel: dto.hsk_level,
    translation: matchedTranslation
      ? matchedTranslation.translation
      : fallbackTranslation,
  };
}

export async function getWords(
  hskLevel: number,
  lang: string = "ru",
): Promise<Word[]> {
  const url = `${API_URL}/api/v1/words?hsk_level=${hskLevel}`;

  try {
    const response = await fetch(url, {
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const rawData: WordDTO[] = await response.json();

    return rawData.map((dto) => mapWordDtoToDomain(dto, lang));
  } catch (error) {
    console.error("Failed to fetch words:", error);
    throw error;
  }
}
