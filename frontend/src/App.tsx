// src/App.tsx
import { useState } from "react";
import "./App.css";

import Sidebar from "./components/Sidebar";
import AuthModal from "./components/AuthModal";

import Readme from "./pages/Readme";
import Words from "../src/pages/Words";
import Dictionary from "./pages/Dictionary";

function App() {
  const [currentPage, setCurrentPage] = useState("readme");
  const [language, setLanguage] = useState("ru");
  const [isAuthOpen, setIsAuthOpen] = useState(false);

  return (
    <div className="app">
      <Sidebar
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        language={language}
        setLanguage={setLanguage}
        openAuth={() => setIsAuthOpen(true)}
      />

      <main className="main">
        {currentPage === "readme" && <Readme language={language} />}
        {currentPage === "words" && <Words setCurrentPage={setCurrentPage} />}
        {currentPage === "dictionary" && <Dictionary />}
      </main>

      {isAuthOpen && <AuthModal onClose={() => setIsAuthOpen(false)} />}
    </div>
  );
}

export default App;
