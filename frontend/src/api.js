// Base URL of the FastAPI backend. During local development this points at
// uvicorn's default port; set VITE_API_URL in a .env file to override it
// once the backend is deployed (Milestone 5).
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function fetchRecommendations(answers) {
  const response = await fetch(`${API_URL}/api/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(answers),
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new Error(detail?.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}
