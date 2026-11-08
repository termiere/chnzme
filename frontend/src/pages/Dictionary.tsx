// src/pages/Dictionary.tsx
import { useEffect, useState, useMemo } from "react";
import { ChevronLeft, Search } from "lucide-react";
import { Link } from "react-router-dom";

import ru from "../locales/ru";
import en from "../locales/en";

import WordItem from "../components/WordItem";
import { getUserWords, deleteUserWord } from "../api/userWords";
import type { UserWord } from "../types/userWords";
import { matchesWord } from "../utils/searchWords";

import "../styles/Words.css";

type DictionaryProps = {
  language: string;
};

function Dictionary({ language }: DictionaryProps) {
  const text = language === "ru" ? ru.dictionary : en.dictionary;
  const [userWords, setUserWords] = useState<UserWord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");

  const filteredWords = useMemo(
    () => userWords.filter((uw) => matchesWord(uw.word, query)),
    [userWords, query],
  );

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    getUserWords(language)
      .then((data) => {
        if (isMounted) setUserWords(data);
      })
      .catch((err) => {
        if (isMounted) setError(err.message || text.errorLoading);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [language]);

  const handleDelete = async (wordId: number) => {
    const previousWords = [...userWords];
    setUserWords((currentWords) =>
      currentWords.filter((item) => item.word.id !== wordId),
    );

    try {
      await deleteUserWord(wordId);
    } catch (err) {
      console.error(err);
      alert(text.deleteError);
      setUserWords(previousWords);
    }
  };

  if (loading) return <div>{text.loading}</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <section className="dictionary">
      <h1>#dictionary</h1>

      <div className="hsk-actions">
        <Link to="/words" className="back-to-levels-card">
          <ChevronLeft size={18} />
          <span>{text.back}</span>
        </Link>

        <div className="search-card">
          <Search size={18} />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={text.search}
          />
        </div>
      </div>

      {userWords.length === 0 ? (
        <p>{text.empty}</p>
      ) : filteredWords.length === 0 ? (
        <p>{text.noWords}</p>
      ) : (
        <div className="dictionary-list">
          {filteredWords.map((userWord) => (
            <WordItem
              key={userWord.userWordId}
              hanzi={userWord.word.character}
              pinyin={userWord.word.pinyin}
              translation={userWord.word.translation}
              status={userWord.status}
              nextReview={userWord.nextReview}
              onDelete={() => handleDelete(userWord.word.id)}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default Dictionary;
