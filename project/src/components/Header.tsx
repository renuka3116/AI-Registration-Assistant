import { Bot, Sparkles } from "lucide-react";

export default function Header() {
  return (
    <header className="flex items-center gap-3 border-b border-slate-200 bg-white/80 px-6 py-4 backdrop-blur">
      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 shadow-lg shadow-blue-500/20">
        <Bot className="h-6 w-6 text-white" />
      </div>
      <div className="flex-1">
        <h1 className="text-lg font-semibold text-slate-900">AI Registration Assistant</h1>
        <p className="text-sm text-slate-500">Your intelligent internship registration companion</p>
      </div>
      <div className="hidden items-center gap-1.5 rounded-full bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700 sm:flex">
        <Sparkles className="h-3.5 w-3.5" />
        NLP Powered
      </div>
    </header>
  );
}
