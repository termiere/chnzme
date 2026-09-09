import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import ProfileOverlay from "./ProfileOverlay";
import LanguageSelector from "./LanguageSelector";

type SidebarProps = {
  currentPage: string;
  setCurrentPage: (page: string) => void;
  language: string;
  setLanguage: (language: string) => void;
  openAuth: () => void;
};

function Sidebar({
  currentPage,
  setCurrentPage,
  language,
  setLanguage,
  openAuth,
}: SidebarProps) {
  const { user } = useAuth();

  const [isProfileOpen, setIsProfileOpen] = useState(false);

  return (
    <>
      <aside className="sidebar">
        <h2>CHNZME</h2>

        <nav>
          <button
            className={currentPage === "readme" ? "active" : ""}
            onClick={() => setCurrentPage("readme")}
          >
            README.md
          </button>

          <button
            className={currentPage === "words" ? "active" : ""}
            onClick={() => setCurrentPage("words")}
          >
            Words
          </button>
        </nav>

        <div className="sidebar-bottom">
          {user ? (
            <button
              className="profile-username"
              onClick={() => setIsProfileOpen(true)}
            >
              {user.username}
            </button>
          ) : (
            <button className="login-button" onClick={openAuth}>
              Sign in
            </button>
          )}

          <LanguageSelector language={language} setLanguage={setLanguage} />
        </div>
      </aside>

      {isProfileOpen && (
        <ProfileOverlay onClose={() => setIsProfileOpen(false)} />
      )}
    </>
  );
}

export default Sidebar;
