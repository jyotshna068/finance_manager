import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api, saveAuth } from "../utils/api";

export default function Register() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.register(form);
      saveAuth(res.access_token, res.user_id);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-xl shadow-sm w-full max-w-sm">
        <h1 className="text-xl font-semibold text-slate-900 mb-1">Create an account</h1>
        <p className="text-sm text-slate-500 mb-6">Start managing your finances with AI</p>

        {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

        <input
          type="text"
          placeholder="Full Name"
          required
          className="w-full border border-slate-300 rounded-lg px-3 py-2 mb-3 text-sm"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          required
          className="w-full border border-slate-300 rounded-lg px-3 py-2 mb-3 text-sm"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          required
          className="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 text-sm"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-slate-900 text-white rounded-lg py-2 text-sm font-medium hover:bg-slate-800 transition disabled:opacity-50"
        >
          {loading ? "Creating account..." : "Sign Up"}
        </button>

        <p className="text-sm text-slate-500 mt-4 text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-slate-900 font-medium">
            Log in
          </Link>
        </p>
      </form>
    </div>
  );
}
