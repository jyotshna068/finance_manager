import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api, saveAuth } from "../utils/api";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.login(form);
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
        <h1 className="text-xl font-semibold text-slate-900 mb-1">Welcome back</h1>
        <p className="text-sm text-slate-500 mb-6">Log in to your finance dashboard</p>

        {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

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
          {loading ? "Logging in..." : "Log In"}
        </button>

        <p className="text-sm text-slate-500 mt-4 text-center">
          Don't have an account?{" "}
          <Link to="/register" className="text-slate-900 font-medium">
            Sign up
          </Link>
        </p>
      </form>
    </div>
  );
}
