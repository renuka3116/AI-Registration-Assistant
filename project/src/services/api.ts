// API service - communicates with the Python Flask backend.

const API_BASE = "http://localhost:5000";

export interface ChatResponse {
  response: string;
  intent: string;
  confidence: number;
  entities: Record<string, string>;
  registration_state: string;
  registration_data?: {
    name?: string;
    email?: string;
    field?: string;
    experience?: string;
  };
}

export interface Registration {
  id: number;
  name: string;
  email: string;
  field: string;
  experience: string;
  registered_at: string;
}

/** Check if the backend is running. */
export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (!res.ok) return false;
    const data = await res.json();
    return data.status === "running";
  } catch {
    return false;
  }
}

/** Send a chat message to the backend and return the chatbot response. */
export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.error || "Failed to get a response from the assistant.");
  }

  return res.json();
}

/** Reset the conversation state on the backend. */
export async function resetConversation(): Promise<void> {
  try {
    await fetch(`${API_BASE}/api/reset`, { method: "POST" });
  } catch {
    // non-critical
  }
}

/** Fetch all stored registrations. */
export async function getRegistrations(): Promise<Registration[]> {
  const res = await fetch(`${API_BASE}/api/registrations`);
  if (!res.ok) throw new Error("Failed to fetch registrations.");
  const data = await res.json();
  return data.registrations;
}
