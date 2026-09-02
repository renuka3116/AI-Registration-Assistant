import { Brain, Target, ScanText, MailCheck, MessagesSquare, Database, HelpCircle, Smartphone } from "lucide-react";

const features = [
  { icon: Brain, title: "NLP Processing", desc: "Text preprocessing with NLTK: tokenization, stopword removal, and lemmatization." },
  { icon: Target, title: "Intent Recognition", desc: "TF-IDF vectorization + Logistic Regression to classify what the user wants." },
  { icon: ScanText, title: "Entity Extraction", desc: "Regex-based extraction of name, email, field of study, and experience level." },
  { icon: MailCheck, title: "Email Validation", desc: "Validates email format before proceeding with the registration flow." },
  { icon: MessagesSquare, title: "Conversational Registration", desc: "Multi-turn dialog management guides students step by step through registration." },
  { icon: Database, title: "JSON Data Storage", desc: "Confirmed registrations persist in a local JSON file — no external database required." },
  { icon: HelpCircle, title: "Unknown Intent Handling", desc: "Low-confidence predictions trigger a graceful rephrase request." },
  { icon: Smartphone, title: "Responsive Web Interface", desc: "Works seamlessly on desktop, tablet, and mobile devices." },
];

export default function FeaturesView() {
  return (
    <div className="h-full overflow-y-auto bg-slate-50 p-6 sm:p-8">
      <div className="mx-auto w-full max-w-5xl">
        <h2 className="mb-6 text-xl font-semibold text-slate-900">Project Features</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => {
            const Icon = f.icon;
            return (
              <div key={f.title} className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200 transition hover:shadow-md">
                <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400">
                  <Icon className="h-5 w-5 text-white" />
                </div>
                <h3 className="text-sm font-semibold text-slate-900">{f.title}</h3>
                <p className="mt-1 text-sm text-slate-500">{f.desc}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
