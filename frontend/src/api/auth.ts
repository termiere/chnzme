const API_URL = import.meta.env.VITE_API_URL;

export async function registerUser(username: string, password: string) {
  const response = await fetch(`${API_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new Error(
      typeof data?.detail === "string" ? data.detail : "Registration failed",
    );
  }
}
