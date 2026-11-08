import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";

import ru from "../locales/ru";
import en from "../locales/en";

import "../styles/ProfileOverlay.css";

type ProfileProps = {
  language: string;
  onClose: () => void;
};

function Profile({ language, onClose }: ProfileProps) {
  const text = language === "ru" ? ru.profile : en.profile;
  const { user, logout } = useAuth();

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  if (!user) return null;

  const handleLogout = () => {
    logout();
    onClose();
  };

  return (
    <div className="profile-overlay" onClick={onClose}>
      <div className="profile-modal" onClick={(e) => e.stopPropagation()}>
        <div className="profile-header">
          <div className="profile-info">
            <h1>#profile</h1>
            <span className="profile-info-username">##{user.username}</span>
          </div>

          <button
            className="profile-close"
            onClick={onClose}
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <button className="profile-logout" onClick={handleLogout}>
          {text.logout}
        </button>
      </div>
    </div>
  );
}

export default Profile;
