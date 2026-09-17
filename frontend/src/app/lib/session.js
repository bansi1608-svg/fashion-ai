// frontend/src/app/lib/session.js
//
// Manages an anonymous session ID, stored in the browser, so we can
// recognize "this same browser searched for X before" without any
// login/signup system.

const SESSION_KEY = "fashion_ai_session_id";

export function getSessionId() {
  // This only works in the browser, not during server-side rendering -
  // guard against that.
  if (typeof window === "undefined") return null;

  let sessionId = localStorage.getItem(SESSION_KEY);

  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, sessionId);
  }

  return sessionId;
}