// frontend/src/app/lib/interactions.js
//
// Fire-and-forget interaction logging - never blocks or breaks the
// user's actual experience, even if logging itself fails.

import { getSessionId } from "./session";

const API_BASE_URL = "http://127.0.0.1:8000";

export function logInteraction({ interactionType, style, colour, category, productId }) {
  const sessionId = getSessionId();
  if (!sessionId) return;

  fetch(`${API_BASE_URL}/interactions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      interaction_type: interactionType,
      style: style ?? null,
      colour: colour ?? null,
      category: category ?? null,
      product_id: productId ?? null,
    }),
  }).catch((err) => {
    console.warn("Failed to log interaction:", err);
  });
}