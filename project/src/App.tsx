import { useState, useCallback } from "react";
import { Menu, Trash2, Wifi, WifiOff } from "lucide-react";
import Sidebar, { type SidebarView } from "./components/Sidebar";
import Header from "./components/Header";
import ChatWindow, { type ChatMessage } from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import RegistrationSummary from "./components/RegistrationSummary";
import AboutView from "./components/AboutView";
import FeaturesView from "./components/FeaturesView";
import { sendChatMessage, resetConversation, getRegistrations, type Registration } from "./services/api";

const WELCOME_MESSAGE: ChatMessage = {
  id: "welcome",
  role: "assistant",
  text: "Hello! 👋 Welcome to the AI Registration Assistant.\n\nI can help you with internship registration, required information, internship details, and application-related queries.\n\nWould you like to register for the internship?",
  timestamp: new Date(),
};

const QUICK_ACTIONS = [
  { label: "Register Now", message: "I want to register for the internship" },
  { label: "Internship Details", message: "Tell me about the internship" },
  { label: "Requirements", message: "What are the requirements?" },
  { label: "Help", message: "Help" },
];

function uid() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export default function App() {
  const [view, setView] = useState<SidebarView>("chat");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [isTyping, setIsTyping] = useState(false);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const [registrations, setRegistrations] = useState<Registration[]>([]);
  const [regLoading, setRegLoading] = useState(false);
  const [regError, setRegError] = useState<string | null>(null);

  const handleSend = useCallback(async (text: string) => {
    const userMsg: ChatMessage = {
      id: uid(),
      role: "user",
      text,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);
    setBackendOnline(null);

    try {
      const res = await sendChatMessage(text);
      setBackendOnline(true);

      // Detect if the response contains a registration summary (multi-line with Name: ...)
      const isSummary =
        res.registration_state === "confirmation" &&
        !!res.registration_data &&
        !!res.registration_data.name;

      const assistantMsg: ChatMessage = {
        id: uid(),
        role: "assistant",
        text: res.response,
        timestamp: new Date(),
        registrationData: res.registration_data,
        showSummary: isSummary,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setBackendOnline(false);
      const errorMsg: ChatMessage = {
        id: uid(),
        role: "assistant",
        text: "I couldn't reach the backend server. Please make sure the Flask backend is running on http://localhost:5000.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  }, []);

  const handleClearChat = useCallback(async () => {
    setMessages([WELCOME_MESSAGE]);
    setBackendOnline(null);
    await resetConversation();
  }, []);

  const handleQuickAction = useCallback(
    (message: string) => {
      handleSend(message);
    },
    [handleSend]
  );

  const loadRegistrations = useCallback(async () => {
    setRegLoading(true);
    setRegError(null);
    try {
      const regs = await getRegistrations();
      setRegistrations(regs);
    } catch {
      setRegError("Could not load registrations. Is the backend running?");
    } finally {
      setRegLoading(false);
    }
  }, []);

  const handleNavigate = useCallback(
    (next: SidebarView) => {
      setView(next);
      if (next === "registration") {
        loadRegistrations();
      }
    },
    [loadRegistrations]
  );

  return (
    <div className="flex h-screen overflow-hidden bg-slate-100">
      <Sidebar
        active={view}
        onNavigate={handleNavigate}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Mobile top bar */}
        <div className="flex items-center gap-3 border-b border-slate-200 bg-white px-4 py-3 lg:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-600 hover:bg-slate-100"
          >
            <Menu className="h-5 w-5" />
          </button>
          <span className="text-sm font-semibold text-slate-900">AI Registration Assistant</span>
        </div>

        {view === "chat" && (
          <>
            <Header />
            <ChatWindow messages={messages} isTyping={isTyping} />

            {/* Quick actions (only show when just the welcome message is present) */}
            {messages.length <= 1 && !isTyping && (
              <div className="flex flex-wrap gap-2 border-t border-slate-200 bg-white px-4 py-3">
                {QUICK_ACTIONS.map((qa) => (
                  <button
                    key={qa.label}
                    onClick={() => handleQuickAction(qa.message)}
                    className="rounded-full bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 ring-1 ring-blue-200 transition hover:bg-blue-100"
                  >
                    {qa.label}
                  </button>
                ))}
              </div>
            )}

            {/* Status + clear chat bar */}
            <div className="flex items-center justify-between gap-2 border-t border-slate-200 bg-white px-4 py-2">
              <div className="flex items-center gap-1.5 text-xs">
                {backendOnline === null && <span className="text-slate-400">Backend: not checked</span>}
                {backendOnline === true && (
                  <span className="flex items-center gap-1 text-green-600">
                    <Wifi className="h-3.5 w-3.5" /> Backend connected
                  </span>
                )}
                {backendOnline === false && (
                  <span className="flex items-center gap-1 text-red-500">
                    <WifiOff className="h-3.5 w-3.5" /> Backend offline
                  </span>
                )}
              </div>
              <button
                onClick={handleClearChat}
                className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium text-slate-600 transition hover:bg-slate-100"
              >
                <Trash2 className="h-3.5 w-3.5" />
                Clear Chat
              </button>
            </div>

            <ChatInput onSend={handleSend} disabled={isTyping} />
          </>
        )}

        {view === "registration" && (
          <RegistrationSummary
            registrations={registrations}
            loading={regLoading}
            error={regError}
            onRefresh={loadRegistrations}
          />
        )}

        {view === "about" && <AboutView />}
        {view === "features" && <FeaturesView />}
      </div>
    </div>
  );
}
