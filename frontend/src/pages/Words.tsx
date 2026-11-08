import { useEffect, useMemo, useState } from "react";
import { ChevronLeft, Search } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import ru from "../locales/ru";
import en from "../locales/en";

import { useWords } from "../hooks/useWords";
import { useHskStats } from "../hooks/useHskStats";
import { addUserWord, getUserWords } from "../api/userWords";
import { WordList } from "../components/WordList";
import AuthModal from "../components/AuthModal";
import { useAuth } from "../context/AuthContext";
import { matchesWord } from "../utils/searchWords";

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
  const { stats: selectedHskStats } = useHskStats(user ? selectedHsk : null);
  const [query, setQuery] = useState("");

  const [userWordIds, setUserWordIds] = useState<Set<number>>(new Set());
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const {
    data: words,
    isLoading,
    isError,
    error,
  } = useWords(selectedHsk, language);

  const filteredWords = useMemo(
    () => words?.filter((w) => matchesWord(w, query)),
    [words, query],
  );

  useEffect(() => {
    setQuery("");
  }, [selectedHsk]);

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

              {selectedHskStats && (
                <div className="hsk-progress-card">
                  <span>
                    {selectedHskStats.added_words_count}/
                    {selectedHskStats.total_words_count}
                  </span>
                </div>
              )}
            </div>

            {isLoading && <div className="words-loading">{text.loading}</div>}

            {isError && (
              <div className="error-message">
                <strong>{text.errorLoading}</strong> {error?.message}
              </div>
            )}

            {words &&
              filteredWords &&
              (filteredWords.length === 0 ? (
                <p>{text.noWords}</p>
              ) : (
                <WordList
                  words={filteredWords}
                  userWordIds={userWordIds}
                  isAuthenticated={!!user}
                  onAddWord={handleAddWord}
                  onLoginRequired={() => setIsAuthModalOpen(true)}
                  language={language}
                />
              ))}
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
