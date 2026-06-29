import { formatCurrency, formatPercent } from "../utils/formatters";

export default function BudgetTable({ variance }) {
  const entries = Object.entries(variance || {});

  if (entries.length === 0) {
    return <p className="text-sm text-slate-400">No budget data available yet.</p>;
  }

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="text-left text-slate-500 border-b border-slate-200">
          <th className="py-2">Category</th>
          <th className="py-2">Planned</th>
          <th className="py-2">Actual</th>
          <th className="py-2">Variance</th>
          <th className="py-2">Status</th>
        </tr>
      </thead>
      <tbody>
        {entries.map(([category, v]) => (
          <tr key={category} className="border-b border-slate-100">
            <td className="py-2 capitalize">{category}</td>
            <td className="py-2">{formatCurrency(v.planned)}</td>
            <td className="py-2">{formatCurrency(v.actual)}</td>
            <td className="py-2">{formatPercent(v.variance_percent)}</td>
            <td className="py-2">
              <span
                className={`text-xs font-medium px-2 py-1 rounded-full ${
                  v.overspent ? "text-red-600 bg-red-50" : "text-emerald-600 bg-emerald-50"
                }`}
              >
                {v.overspent ? "Overspent" : "On Track"}
              </span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
