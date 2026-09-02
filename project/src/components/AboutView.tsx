import { Info, Brain, Code, Layers } from "lucide-react";

const technologies = ["Python", "NLP", "NLTK", "Scikit-learn", "TF-IDF", "Logistic Regression", "Flask", "React", "JSON"];
const concepts = ["Intent Classification", "Entity Extraction", "Dialog Management", "Validation", "Conversational AI"];

export default function AboutView() {
  return (
    <div className="h-full overflow-y-auto bg-slate-50 p-6 sm:p-8">
      <div className="mx-auto w-full max-w-4xl space-y-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-100">
            <Info className="h-5 w-5 text-blue-600" />
          </div>
          <h2 className="text-xl font-semibold text-slate-900">About This Project</h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <h3 className="text-base font-semibold text-slate-900">Project Name</h3>
          <p className="mt-1 text-slate-600">AI Registration Assistant</p>

          <h3 className="mt-5 text-base font-semibold text-slate-900">Purpose</h3>
          <p className="mt-1 text-slate-600">
            An NLP-based conversational chatbot designed to guide students through internship registration.
            It understands natural-language queries, recognizes user intent, extracts and validates student
            information, and stores confirmed registrations — all without any paid external AI API.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <div className="mb-3 flex items-center gap-2">
              <Code className="h-5 w-5 text-blue-600" />
              <h3 className="text-base font-semibold text-slate-900">Technologies</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {technologies.map((t) => (
                <span key={t} className="rounded-lg bg-blue-50 px-3 py-1.5 text-sm font-medium text-blue-700">
                  {t}
                </span>
              ))}
            </div>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <div className="mb-3 flex items-center gap-2">
              <Brain className="h-5 w-5 text-blue-600" />
              <h3 className="text-base font-semibold text-slate-900">Core Concepts</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {concepts.map((c) => (
                <span key={c} className="rounded-lg bg-cyan-50 px-3 py-1.5 text-sm font-medium text-cyan-700">
                  {c}
                </span>
              ))}
            </div>
          </div>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <div className="mb-3 flex items-center gap-2">
            <Layers className="h-5 w-5 text-blue-600" />
            <h3 className="text-base font-semibold text-slate-900">Architecture</h3>
          </div>
          <p className="text-sm leading-relaxed text-slate-600">
            The frontend (React + Vite) sends user messages to the Flask backend via REST API.
            The backend preprocesses the text with NLTK (tokenization, stopword removal, lemmatization),
            vectorizes it with TF-IDF, and classifies the intent using a Logistic Regression model trained
            on the intents dataset. A dialog manager tracks the conversation state and guides the student
            through registration. Entities like name, email, field, and experience are extracted with
            regex patterns. Confirmed registrations are stored in a JSON file.
          </p>
        </div>
      </div>
    </div>
  );
}
