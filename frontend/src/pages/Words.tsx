// src/pages/Words.tsx
import { useEffect, useState } from "react";
import { useWords } from "../hooks/useWords";
import { addUserWord, getUserWords } from "../api/userWords";
import { WordList } from "../components/WordList";
import AuthModal from "../components/AuthModal";
import { useAuth } from "../context/AuthContext";

type WordsProps = {
  setCurrentPage: (page: string) => void;
};

const HSK_LEVELS = [
  { level: 1, title: "HSK 1", description: "Beginner vocabulary" },
  { level: 2, title: "HSK 2", description: "Elementary vocabulary" },
  { level: 3, title: "HSK 3", description: "Intermediate vocabulary" },
];

function Words({ setCurrentPage }: WordsProps) {
  const { user } = useAuth();
  const [selectedHsk, setSelectedHsk] = useState<number | null>(null);
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
  // Функция добавления слова в изученные через сервис userWords
  const handleAddWord = async (wordId: number) => {
    try {
      await addUserWord(wordId);
    } catch (err) {
      console.error(`Failed to add word ${wordId}:`, err);
      throw err; // Пробрасываем ошибку, чтобы компонент WordList мог откатить UI
    }
  };

  return (
    <section className="words-page">
      <h1># Words</h1>

      <section className="words-section">
        <h2>## Study</h2>

        <div className="words-list">
          <button
            className="words-block"
            onClick={() => setCurrentPage("review")}
          >
            <span className="words-block-title">Review</span>
            <span className="words-block-description">Repeat words</span>
          </button>

          <button
            className="words-block"
            onClick={() => setCurrentPage("dictionary")}
          >
            <span className="words-block-title">Dictionary</span>
            <span className="words-block-description">All words</span>
          </button>
        </div>
      </section>

      <section className="words-section">
        <div className="section-header">
          <h2>## HSK</h2>
          {selectedHsk && (
            <button
              className="back-to-levels-card"
              onClick={() => setSelectedHsk(null)}
            >
              {/* <span className="back-to-levels-arrow"></span> */}
              <span>Back to levels</span>
            </button>
          )}
        </div>

        {!selectedHsk ? (
          <div className="words-list">
            {HSK_LEVELS.map(({ level, title, description }) => (
              <button
                key={level}
                className="words-block"
                onClick={() => setSelectedHsk(level)}
              >
                <span className="words-block-title">{title}</span>
                <span className="words-block-description">{description}</span>
              </button>
            ))}
          </div>
        ) : (
          <div className="hsk-content">
            <h3>Vocabulary for HSK {selectedHsk}</h3>

            {isLoading && <div className="words-loading">Loading words...</div>}

            {isError && (
              <div
                style={{
                  color: "red",
                  padding: "10px",
                  border: "1px solid red",
                }}
              >
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
