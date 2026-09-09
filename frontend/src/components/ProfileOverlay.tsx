import { useAuth } from "../context/AuthContext";
import "./ProfileOverlay.css";

type ProfileOverlayProps = {
  onClose: () => void;
};

function ProfileOverlay({ onClose }: ProfileOverlayProps) {
  const { user, logout } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className="profile-overlay" onClick={onClose}>
      <div
        className="profile-modal"
        onClick={(event) => event.stopPropagation()}
      >
        <button className="profile-close" onClick={onClose}>
          ×
        </button>

        <div className="profile-header">
          <div className="profile-photo">
            <span>+</span>
          </div>

          <div className="profile-info">
            <h3 className="profile-info-username">@{user.username}</h3>

            <p className="profile-about">Nothing here yet.</p>
          </div>
        </div>

        <button
          className="profile-logout"
          onClick={() => {
            logout();
            onClose();
          }}
        >
          Log out
        </button>
      </div>
    </div>
  );
}

export default ProfileOverlay;
