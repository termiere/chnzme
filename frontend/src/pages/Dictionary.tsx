// src/pages/Dictionary.tsx
import { useEffect, useState } from "react";
import { ChevronLeft } from "lucide-react";
import { Link } from "react-router-dom";

import ru from "../locales/ru";
import en from "../locales/en";

import WordItem from "../components/WordItem";
import { type UserWord, getUserWords, deleteUserWord } from "../api/userWords";

import "../styles/Words.css";

type DictionaryProps = {
  language: string;
};

function Dictionary({ language }: DictionaryProps) {
  const text = language === "ru" ? ru.dictionary : en.dictionary;
  const [userWords, setUserWords] = useState<UserWord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

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

      <Link to="/words" className="back-to-levels-card">
        <ChevronLeft />
        <span>{text.back}</span>
      </Link>

      {userWords.length === 0 ? (
        <p>{text.empty}</p>
      ) : (
        <div className="dictionary-list">
          {userWords.map((userWord) => (
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
