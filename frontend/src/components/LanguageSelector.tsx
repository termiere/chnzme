import { useState } from "react";

type LanguageSelectorProps = {
  language: string;
  setLanguage: (language: string) => void;
};

const languages = [
  { code: "ru", label: "RU" },
  { code: "en", label: "EN" },
];

function LanguageSelector({ language, setLanguage }: LanguageSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="language-container">
      <button
        className={`language-button ${isOpen ? "active" : ""}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        {languages.find((item) => item.code === language)?.label ?? language}
      </button>

      {isOpen && (
        <div className="language-dropdown">
          {languages.map((item) => (
            <button
              key={item.code}
              className={`language-option ${
                language === item.code ? "selected" : ""
              }`}
              onClick={() => {
                setLanguage(item.code);
                setIsOpen(false);
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default LanguageSelector;
