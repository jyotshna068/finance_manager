import { useState } from "react";
import Navbar from "../components/Navbar";
import { api } from "../utils/api";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setStatus("");
    try {
      const res = await api.uploadStatement(file);
      setStatus(`✅ ${res.transactions_inserted} transactions imported from ${res.file_name}`);
    } catch (err) {
      setStatus(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-2xl mx-auto py-12 px-6">
        <h1 className="text-2xl font-semibold text-slate-900 mb-2">Upload a Statement</h1>
        <p className="text-sm text-slate-500 mb-8">
          Supports PDF, CSV, and Excel bank or wallet statements.
        </p>

        <div className="bg-white rounded-xl border border-dashed border-slate-300 p-10 text-center">
          <input
            type="file"
            accept=".pdf,.csv,.xlsx,.xls"
            onChange={(e) => setFile(e.target.files[0])}
            className="block mx-auto mb-4 text-sm"
          />
          {file && <p className="text-sm text-slate-600 mb-4">Selected: {file.name}</p>}

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="bg-slate-900 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-slate-800 transition disabled:opacity-50"
          >
            {loading ? "Processing..." : "Upload & Process"}
          </button>
        </div>

        {status && <p className="text-sm mt-6 text-center">{status}</p>}

        {status.startsWith("✅") && (
          <div className="text-center mt-6">
            <button
              onClick={() => navigate("/dashboard")}
              className="text-sm font-medium text-slate-900 underline"
            >
              Go to Dashboard →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
