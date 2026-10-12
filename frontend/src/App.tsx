// src/App.tsx
import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import "./App.css";

import Sidebar from "./components/Sidebar";
import AuthModal from "./components/AuthModal";

import Readme from "./pages/Readme";
import Words from "../src/pages/Words";
import Dictionary from "./pages/Dictionary";
import Review from "./pages/Review";

function App() {
  const [language, setLanguage] = useState("ru");
  const [isAuthOpen, setIsAuthOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar
          language={language}
          setLanguage={setLanguage}
          openAuth={() => setIsAuthOpen(true)}
        />

        <main className="main">
          <Routes>
            <Route path="/" element={<Readme language={language} />} />
            <Route path="/readme" element={<Readme language={language} />} />
            <Route path="/words" element={<Words language={language} />} />
            <Route
              path="/words/hsk/:level"
              element={<Words language={language} />}
            />
            <Route
              path="/dictionary"
              element={<Dictionary language={language} />}
            />
            <Route path="/review" element={<Review language={language} />} />
          </Routes>
        </main>

        {isAuthOpen && <AuthModal onClose={() => setIsAuthOpen(false)} />}
      </div>
    </BrowserRouter>
  );
}

export default App;
