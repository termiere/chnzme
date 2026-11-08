import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useAuth } from "../context/AuthContext";
import { registerUser } from "../api/auth";

import "../styles/Auth.css";
type Mode = "login" | "register";

type AuthModalProps = {
  onClose: () => void;
};

function AuthModal({ onClose }: AuthModalProps) {
  const { login } = useAuth();

  const [mode, setMode] = useState<Mode>("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const isLogin = mode === "login";

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      if (isLogin) {
        await login(username, password);
      } else {
        await registerUser(username, password);
      }
      setIsSuccess(true);
    } catch (err) {
      if (err instanceof TypeError) {
        setError("Unable to connect to the server");
      } else {
        setError(err instanceof Error ? err.message : "Something went wrong");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const switchMode = (next: Mode) => {
    setMode(next);
    setPassword("");
    setError("");
  };

  return (
    <div className="auth-overlay" onMouseDown={onClose}>
      <div
        className="auth-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="auth-title"
        onMouseDown={(e) => e.stopPropagation()}
      >
        {isSuccess ? (
          <div className="auth-success">
            <div className="auth-success-icon">✓</div>

            <h2 id="auth-title" className="auth-title">
              {isLogin ? "Welcome back" : "Account created"}
            </h2>

            <p>
              {isLogin
                ? "You have successfully signed in."
                : "Your account has been successfully created."}
            </p>

            <button type="button" className="auth-submit" onClick={onClose}>
              Continue
            </button>
          </div>
        ) : (
          <>
            <div className="auth-header">
              <h2 id="auth-title" className="auth-title">
                #{isLogin ? "sign in" : "create account"}
              </h2>

              <button
                type="button"
                className="auth-close"
                onClick={onClose}
                aria-label="Close"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="auth-field">
                <label htmlFor="auth-username">username</label>
                <input
                  id="auth-username"
                  type="text"
                  autoComplete="username"
                  autoFocus
                  placeholder="enter your username"
                  value={username}
                  onChange={(e) => {
                    setUsername(e.target.value);
                    setError("");
                  }}
                  required
                />
              </div>

              <div className="auth-field">
                <label htmlFor="auth-password">password</label>
                <input
                  id="auth-password"
                  type="password"
                  autoComplete={isLogin ? "current-password" : "new-password"}
                  placeholder="enter your password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    setError("");
                  }}
                  required
                />
              </div>

              {error && (
                <div className="auth-error" role="alert">
                  {error}
                </div>
              )}

              <button
                type="submit"
                className="auth-submit"
                disabled={isLoading}
              >
                {isLoading
                  ? "Please wait..."
                  : isLogin
                    ? "sign in"
                    : "create account"}
              </button>
            </form>

            <div className="auth-switch">
              <span>
                {isLogin
                  ? "don't have an account?"
                  : "already have an account?"}
              </span>
              <button
                type="button"
                onClick={() => switchMode(isLogin ? "register" : "login")}
              >
                {isLogin ? "create account" : "sign in"}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default AuthModal;
