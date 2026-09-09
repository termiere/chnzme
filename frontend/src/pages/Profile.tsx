import { useAuth } from "../context/AuthContext";

function Profile() {
  const { user, logout } = useAuth();

  return (
    <div>
      <h1>{user?.username}</h1>

      <button onClick={logout}>Log out</button>
    </div>
  );
}

export default Profile;
