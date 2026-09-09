import { useState } from "react";

type ChangeLanguageProps = {
  language: string;
  setLanguage: (language: string) => void;
};

function ChangeLanguage({ language, setLanguage }: ChangeLanguageProps) {
  const [isOpen, setIsOpen] = useState(false);

  const languages = ["ru", "en"];

  const handleLanguageChange = (newLanguage: string) => {
    setLanguage(newLanguage);
    setIsOpen(false);
  };

  return (
    <div className="language-container">
      <button
        className={`language-button ${isOpen ? "active" : ""}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        {language.toUpperCase()}
      </button>

      {isOpen && (
        <div className="language-dropdown">
          {languages.map((lang) => (
            <button
              key={lang}
              className={`language-option ${
                language === lang ? "selected" : ""
              }`}
              onClick={() => handleLanguageChange(lang)}
            >
              {lang.toUpperCase()}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default ChangeLanguage;
