import { Link, useNavigate, useLocation } from "react-router-dom";
import { clearAuth } from "../utils/api";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    clearAuth();
    navigate("/login");
  };

  const navItem = (path, label) => (
    <Link
      to={path}
      className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
        location.pathname === path
          ? "bg-slate-900 text-white"
          : "text-slate-600 hover:bg-slate-100"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <nav className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-white">
      <div className="text-lg font-semibold text-slate-900">💰 AI Finance Manager</div>
      <div className="flex items-center gap-2">
        {navItem("/dashboard", "Dashboard")}
        {navItem("/upload", "Upload")}
        {navItem("/reports", "Reports")}
        <button
          onClick={handleLogout}
          className="ml-4 px-4 py-2 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
