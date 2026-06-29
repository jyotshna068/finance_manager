export default function StatCard({ label, value, sublabel, accent = "slate" }) {
  const accentMap = {
    slate: "border-slate-200 text-slate-900",
    red: "border-red-200 text-red-600",
    emerald: "border-emerald-200 text-emerald-600",
    amber: "border-amber-200 text-amber-600",
  };

  return (
    <div className={`rounded-xl border ${accentMap[accent]} bg-white p-5 shadow-sm`}>
      <p className="text-sm text-slate-500">{label}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
      {sublabel && <p className="text-xs text-slate-400 mt-1">{sublabel}</p>}
    </div>
  );
}
