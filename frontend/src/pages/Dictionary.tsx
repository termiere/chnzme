// src/pages/Dictionary.tsx
import { useEffect, useState } from "react";
import WordItem from "../components/WordItem";
import { type UserWord, getUserWords, deleteUserWord } from "../api/userWords";

import "../components/Words.css";

function Dictionary() {
  const [userWords, setUserWords] = useState<UserWord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    getUserWords()
      .then((data) => {
        if (isMounted) setUserWords(data);
      })
      .catch((err) => {
        if (isMounted) setError(err.message || "Ошибка загрузки словаря");
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const handleDelete = async (wordId: number) => {
    // 1. Оптимистично удаляем слово из UI
    const previousWords = [...userWords];
    setUserWords((currentWords) =>
      currentWords.filter((item) => item.word.id !== wordId),
    );

    try {
      // 2. Вызываем DELETE /user-words/{word_id}
      await deleteUserWord(wordId);
    } catch (err) {
      console.error(err);
      alert("Не удалось удалить слово. Попробуйте снова.");
      // 3. Откатываем UI назад в случае ошибки
      setUserWords(previousWords);
    }
  };

  if (loading) return <div>Загрузка вашего словаря...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <section className="dictionary">
      <h1># Dictionary</h1>

      {userWords.length === 0 ? (
        <p>Ваш словарь пуст. Добавьте слова в разделе HSK!</p>
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
