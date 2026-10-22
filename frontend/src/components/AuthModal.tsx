import { useState } from "react";
import { useAuth } from "../context/AuthContext";

type AuthModalProps = {
  onClose: () => void;
};

function AuthModal({ onClose }: AuthModalProps) {
  const { login } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [isSuccess, setIsSuccess] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL;

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    setError("");
    setIsLoading(true);

    try {
      if (isLogin) {
        await login(username, password);

        setIsSuccess(true);

        return;
      }

      const response = await fetch(`${API_URL}/api/v1/auth/register`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          username,
          password,
        }),
      });

      if (!response.ok) {
        const data = await response.json();

        setError(
          typeof data.detail === "string" ? data.detail : "Registration failed",
        );

        return;
      }

      setIsSuccess(true);
    } catch {
      setError("Unable to connect to the server");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSwitch = (login: boolean) => {
    setIsLogin(login);
    setError("");
  };

  return (
    <div className="auth-overlay" onClick={onClose}>
      <div className="auth-modal" onClick={(event) => event.stopPropagation()}>
        <button className="auth-close" onClick={onClose}>
          ×
        </button>

        {isSuccess ? (
          <div className="auth-success">
            <div className="auth-success-icon">✓</div>

            <h2>{isLogin ? "Welcome back" : "Account created"}</h2>

            <p>
              {isLogin
                ? "You have successfully signed in."
                : "Your account has been successfully created."}
            </p>

            <button className="auth-submit" onClick={onClose}>
              Continue
            </button>
          </div>
        ) : (
          <>
            <h2>{isLogin ? "Sign in" : "Create account"}</h2>

            <form onSubmit={handleSubmit}>
              <div className="auth-field">
                <label>Username</label>

                <input
                  type="text"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(event) => {
                    setUsername(event.target.value);
                    setError("");
                  }}
                  required
                />
              </div>

              <div className="auth-field">
                <label>Password</label>

                <input
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(event) => {
                    setPassword(event.target.value);
                    setError("");
                  }}
                  required
                />
              </div>

              {error && <div className="auth-error">{error}</div>}

              <button
                type="submit"
                className="auth-submit"
                disabled={isLoading}
              >
                {isLoading
                  ? "Please wait..."
                  : isLogin
                    ? "Sign in"
                    : "Create account"}
              </button>
            </form>

            <div className="auth-switch">
              {isLogin ? (
                <>
                  <span>Don't have an account?</span>

                  <button onClick={() => handleSwitch(false)}>
                    Create account
                  </button>
                </>
              ) : (
                <>
                  <span>Already have an account?</span>

                  <button onClick={() => handleSwitch(true)}>Sign in</button>
                </>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default AuthModal;
