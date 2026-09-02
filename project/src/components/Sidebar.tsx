import { Bot, MessageSquare, FileText, Info, Star } from "lucide-react";

export type SidebarView = "chat" | "registration" | "about" | "features";

interface SidebarProps {
  active: SidebarView;
  onNavigate: (view: SidebarView) => void;
  isOpen: boolean;
  onClose: () => void;
}

const navItems: { id: SidebarView; label: string; icon: typeof Bot }[] = [
  { id: "chat", label: "Chat", icon: MessageSquare },
  { id: "registration", label: "Registration", icon: FileText },
  { id: "about", label: "About Project", icon: Info },
  { id: "features", label: "Features", icon: Star },
];

export default function Sidebar({ active, onNavigate, isOpen, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-20 bg-slate-900/50 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed z-30 flex h-full w-72 flex-col bg-slate-900 text-white transition-transform duration-300 lg:static lg:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Brand */}
        <div className="flex items-center gap-3 border-b border-slate-700/50 px-6 py-6">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 shadow-lg shadow-blue-500/30">
            <Bot className="h-7 w-7 text-white" />
          </div>
          <div>
            <h2 className="text-base font-semibold leading-tight">AI Registration</h2>
            <h2 className="text-base font-semibold leading-tight">Assistant</h2>
            <p className="mt-0.5 text-xs text-blue-300">AI + NLP · Internship Support</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-4 py-6">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = active === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  onClose();
                }}
                className={`flex w-full items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-600/30"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <Icon className="h-5 w-5" />
                {item.label}
              </button>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="border-t border-slate-700/50 px-6 py-4">
          <p className="text-xs text-slate-400">
            B.Tech IT · Industrial Training
          </p>
          <p className="mt-1 text-xs text-slate-500">
            7th Semester Project
          </p>
        </div>
      </aside>
    </>
  );
}
