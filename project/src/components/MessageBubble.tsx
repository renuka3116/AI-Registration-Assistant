interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  timestamp: Date;
  registrationData?: {
    name?: string;
    email?: string;
    field?: string;
    experience?: string;
  };
  showSummary?: boolean;
}

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  const time = message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`flex max-w-[80%] flex-col ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={`rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm ${
            isUser
              ? "rounded-br-md bg-blue-600 text-white"
              : "rounded-bl-md bg-white text-slate-800 ring-1 ring-slate-200"
          }`}
        >
          <p className="whitespace-pre-line">{message.text}</p>

          {/* Registration summary card */}
          {message.showSummary && message.registrationData && (
            <div className="mt-3 rounded-xl bg-slate-50 p-4 ring-1 ring-slate-200">
              <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-blue-600">
                Registration Summary
              </p>
              <dl className="space-y-2 text-sm">
                <div className="flex justify-between gap-4">
                  <dt className="text-slate-500">Name</dt>
                  <dd className="font-medium text-slate-800">{message.registrationData.name || "N/A"}</dd>
                </div>
                <div className="flex justify-between gap-4">
                  <dt className="text-slate-500">Email</dt>
                  <dd className="font-medium text-slate-800 break-all">{message.registrationData.email || "N/A"}</dd>
                </div>
                <div className="flex justify-between gap-4">
                  <dt className="text-slate-500">Field</dt>
                  <dd className="font-medium text-slate-800">{message.registrationData.field || "N/A"}</dd>
                </div>
                <div className="flex justify-between gap-4">
                  <dt className="text-slate-500">Experience</dt>
                  <dd className="font-medium text-slate-800">{message.registrationData.experience || "N/A"}</dd>
                </div>
              </dl>
            </div>
          )}
        </div>
        <span className={`mt-1 px-2 text-xs text-slate-400 ${isUser ? "text-right" : "text-left"}`}>
          {time}
        </span>
      </div>
    </div>
  );
}
