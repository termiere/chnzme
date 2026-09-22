// src/pages/Words.tsx
import { useEffect, useState } from "react";
import { ChevronLeft } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import ru from "../locales/ru";
import en from "../locales/en";

import { useWords } from "../hooks/useWords";
import { addUserWord, getUserWords } from "../api/userWords";
import { WordList } from "../components/WordList";
import AuthModal from "../components/AuthModal";
import { useAuth } from "../context/AuthContext";

const HSK_LEVELS = [
  { level: 1, title: "#hsk1" },
  { level: 2, title: "#hsk2" },
  { level: 3, title: "#hsk3" },
];

type WordsProps = {
  language: string;
};

function Words({ language }: WordsProps) {
  const text = language === "ru" ? ru.words : en.words;

  const { user } = useAuth();
  const { level } = useParams();

  const selectedHsk = level ? Number(level) : null;
  const [userWordIds, setUserWordIds] = useState<Set<number>>(new Set());
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const {
    data: words,
    isLoading,
    isError,
    error,
  } = useWords(selectedHsk, language);

  useEffect(() => {
    if (!user) {
      setUserWordIds(new Set());
      return;
    }

    getUserWords(language)
      .then((userWords) => {
        setUserWordIds(new Set(userWords.map((item) => item.word.id)));
      })
      .catch((error) => {
        console.error(text.errorLoading, error);
      });
  }, [user, language]);

  const handleAddWord = async (wordId: number) => {
    try {
      await addUserWord(wordId, language);
    } catch (err) {
      console.error(`${text.addError} ${wordId}:`, err);
      throw err;
    }
  };

  return (
    <section className="words-page">
      <h1>#words</h1>

      <section className="words-section">
        <h2>##study</h2>

        <div className="words-list">
          <Link to="/review" className="words-block">
            <span className="words-block-title">{text.review}</span>
            <span className="words-block-description">{text.repeatWords}</span>
          </Link>

          <Link to="/dictionary" className="words-block">
            <span className="words-block-title">{text.dictionary}</span>
            <span className="words-block-description">{text.allWords}</span>
          </Link>
        </div>
      </section>

      <section className="words-section">
        {!selectedHsk ? (
          <>
            <h2>##hsk</h2>
            <div className="words-list">
              {HSK_LEVELS.map(({ level, title }) => (
                <Link
                  key={level}
                  to={`/words/hsk/${level}`}
                  className="words-block"
                >
                  <span className="words-block-title">{title}</span>
                  <span className="words-block-description">
                    {text.hskDescriptions[level as 1 | 2 | 3]}
                  </span>
                </Link>
              ))}
            </div>
          </>
        ) : (
          <div className="hsk-content">
            <h1>#hsk{selectedHsk}</h1>

            <Link to="/words" className="back-to-levels-card">
              <ChevronLeft />
              <span>{text.back}</span>
            </Link>

            {isLoading && <div className="words-loading">{text.loading}</div>}

            {isError && (
              <div className="error-message">
                <strong>{text.errorLoading}</strong> {error?.message}
              </div>
            )}

            {words && (
              <WordList
                words={words}
                userWordIds={userWordIds}
                isAuthenticated={!!user}
                onAddWord={handleAddWord}
                onLoginRequired={() => setIsAuthModalOpen(true)}
                language={language}
              />
            )}
          </div>
        )}
      </section>

      {isAuthModalOpen && (
        <AuthModal onClose={() => setIsAuthModalOpen(false)} />
      )}
    </section>
  );
}

export default Words;
