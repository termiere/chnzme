// src/pages/Words.tsx
import { useEffect, useState } from "react";
import { ChevronLeft } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { useWords } from "../hooks/useWords";
import { addUserWord, getUserWords } from "../api/userWords";
import { WordList } from "../components/WordList";
import AuthModal from "../components/AuthModal";
import { useAuth } from "../context/AuthContext";

const HSK_LEVELS = [
  { level: 1, title: "#hsk1", description: "beginner vocabulary" },
  { level: 2, title: "#hsk2", description: "elementary vocabulary" },
  { level: 3, title: "#hsk3", description: "intermediate vocabulary" },
];

function Words() {
  const { user } = useAuth();
  const { level } = useParams();
  const selectedHsk = level ? Number(level) : null;
  const [userWordIds, setUserWordIds] = useState<Set<number>>(new Set());
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const { data: words, isLoading, isError, error } = useWords(selectedHsk);

  useEffect(() => {
    if (!user) {
      setUserWordIds(new Set());
      return;
    }

    getUserWords()
      .then((userWords) => {
        setUserWordIds(new Set(userWords.map((item) => item.word.id)));
      })
      .catch((error) => {
        console.error("Ошибка загрузки словаря:", error);
      });
  }, [user]);

  const handleAddWord = async (wordId: number) => {
    try {
      await addUserWord(wordId);
    } catch (err) {
      console.error(`Failed to add word ${wordId}:`, err);
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
            <span className="words-block-title">review</span>
            <span className="words-block-description">repeat words</span>
          </Link>

          <Link to="/dictionary" className="words-block">
            <span className="words-block-title">dictionary</span>
            <span className="words-block-description">all words</span>
          </Link>
        </div>
      </section>

      <section className="words-section">
        {!selectedHsk ? (
          <>
            <h2>##hsk</h2>
            <div className="words-list">
              {HSK_LEVELS.map(({ level, title, description }) => (
                <Link
                  key={level}
                  to={`/words/hsk/${level}`}
                  className="words-block"
                >
                  <span className="words-block-title">{title}</span>
                  <span className="words-block-description">{description}</span>
                </Link>
              ))}
            </div>
          </>
        ) : (
          <div className="hsk-content">
            <h1>#vocabulary for hsk{selectedHsk}</h1>

            <Link to="/words" className="back-to-levels-card">
              <ChevronLeft />
              <span>back</span>
            </Link>

            {isLoading && <div className="words-loading">Loading words...</div>}

            {isError && (
              <div className="error-message">
                <strong>Ошибка загрузки:</strong> {error?.message}
              </div>
            )}

            {words && (
              <WordList
                words={words}
                userWordIds={userWordIds}
                isAuthenticated={!!user}
                onAddWord={handleAddWord}
                onLoginRequired={() => setIsAuthModalOpen(true)}
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
