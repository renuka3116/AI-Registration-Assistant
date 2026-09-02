import { FileText, CheckCircle2, Mail, Calendar } from "lucide-react";
import type { Registration } from "../services/api";

interface RegistrationSummaryProps {
  registrations: Registration[];
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
}

export default function RegistrationSummary({ registrations, loading, error, onRefresh }: RegistrationSummaryProps) {
  return (
    <div className="flex h-full flex-col bg-slate-50 p-6 sm:p-8">
      <div className="mx-auto w-full max-w-4xl">
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-100">
              <FileText className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-slate-900">Stored Registrations</h2>
              <p className="text-sm text-slate-500">All confirmed registrations saved via JSON storage</p>
            </div>
          </div>
          <button
            onClick={onRefresh}
            className="rounded-lg bg-white px-4 py-2 text-sm font-medium text-blue-600 ring-1 ring-slate-200 transition hover:bg-slate-50"
          >
            Refresh
          </button>
        </div>

        {loading && <p className="text-slate-500">Loading registrations...</p>}

        {error && (
          <div className="rounded-xl bg-red-50 p-4 text-sm text-red-700 ring-1 ring-red-200">
            {error}
          </div>
        )}

        {!loading && !error && registrations.length === 0 && (
          <div className="flex flex-col items-center justify-center rounded-2xl bg-white py-16 ring-1 ring-slate-200">
            <FileText className="h-12 w-12 text-slate-300" />
            <p className="mt-4 text-slate-500">No registrations yet.</p>
            <p className="text-sm text-slate-400">Complete a chat registration to see it here.</p>
          </div>
        )}

        {!loading && !error && registrations.length > 0 && (
          <div className="grid gap-4 sm:grid-cols-2">
            {registrations.map((reg) => (
              <div key={reg.id} className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200 transition hover:shadow-md">
                <div className="mb-4 flex items-center justify-between">
                  <span className="flex items-center gap-1.5 rounded-full bg-green-50 px-3 py-1 text-xs font-medium text-green-700">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Confirmed
                  </span>
                  <span className="text-xs font-medium text-slate-400">#{reg.id}</span>
                </div>
                <h3 className="text-lg font-semibold text-slate-900">{reg.name}</h3>
                <div className="mt-3 space-y-2 text-sm">
                  <p className="flex items-center gap-2 text-slate-600">
                    <Mail className="h-4 w-4 text-slate-400" />
                    {reg.email}
                  </p>
                  <p className="text-slate-600">
                    <span className="text-slate-400">Field:</span> {reg.field}
                  </p>
                  <p className="text-slate-600">
                    <span className="text-slate-400">Experience:</span> {reg.experience}
                  </p>
                  <p className="flex items-center gap-2 text-slate-500">
                    <Calendar className="h-4 w-4 text-slate-400" />
                    {new Date(reg.registered_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
