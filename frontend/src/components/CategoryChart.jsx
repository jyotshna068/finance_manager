import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const COLORS = ["#0f172a", "#2563eb", "#0891b2", "#f59e0b", "#dc2626", "#7c3aed", "#16a34a"];

export default function CategoryChart({ data }) {
  const chartData = Object.entries(data || {}).map(([name, value]) => ({ name, value }));

  if (chartData.length === 0) {
    return <p className="text-sm text-slate-400">No expense data available yet.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie data={chartData} dataKey="value" nameKey="name" outerRadius={100} label>
          {chartData.map((_, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
