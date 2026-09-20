import { useState } from "react";
import { NavLink } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import ProfileOverlay from "./ProfileOverlay";
import LanguageSelector from "./LanguageSelector";

import "../styles/Sidebar.css";

type SidebarProps = {
  language: string;
  setLanguage: (language: string) => void;
  openAuth: () => void;
};

function Sidebar({ language, setLanguage, openAuth }: SidebarProps) {
  const { user } = useAuth();
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  return (
    <>
      <aside className="sidebar">
        <h1>CHNZME</h1>

        <nav>
          <NavLink
            to="/readme"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            README.md
          </NavLink>

          <NavLink
            to="/words"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            words
          </NavLink>
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
              sign in
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
