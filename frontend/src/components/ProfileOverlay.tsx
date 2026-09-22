import { useAuth } from "../context/AuthContext";
import "../styles/ProfileOverlay.css";

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
        <div className="profile-header">
          <div className="profile-info">
            <h3 className="profile-info-username">@{user.username}</h3>
          </div>

          <button
            className="profile-close"
            onClick={onClose}
            aria-label="Close profile"
          >
            ×
          </button>
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
