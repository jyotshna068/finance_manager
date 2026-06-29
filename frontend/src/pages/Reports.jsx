import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { api } from "../utils/api";
import { formatDate } from "../utils/formatters";

export default function Reports() {
  const [history, setHistory] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const res = await api.getReportHistory();
      setHistory(res);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setError("");
    try {
      const blob = await api.generateReport();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "financial_report.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      loadHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-3xl mx-auto py-10 px-6">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-semibold text-slate-900">Reports</h1>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="bg-slate-900 text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-slate-800 transition disabled:opacity-50"
          >
            {generating ? "Generating..." : "Generate New Report"}
          </button>
        </div>

        {error && <p className="text-red-600 text-sm mb-4">{error}</p>}

        <div className="bg-white rounded-xl border border-slate-200 divide-y">
          {history.length === 0 && (
            <p className="p-6 text-sm text-slate-400">No reports generated yet.</p>
          )}
          {history.map((r) => (
            <div key={r.id} className="p-4 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-900">
                  Report #{r.id} — Health Score: {r.health_score}/100
                </p>
                <p className="text-xs text-slate-400">{formatDate(r.generated_at)}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
