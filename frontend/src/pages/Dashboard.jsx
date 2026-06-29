import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import StatCard from "../components/StatCard";
import CategoryChart from "../components/CategoryChart";
import TrendChart from "../components/TrendChart";
import BudgetTable from "../components/BudgetTable";
import RecommendationList from "../components/RecommendationList";
import { api } from "../utils/api";
import { formatCurrency } from "../utils/formatters";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAnalysis();
  }, []);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.getAnalysis();
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <p className="text-center mt-20 text-slate-400">Running multi-agent analysis...</p>
      </div>
    );
  }

  const expense = data?.expense_analysis || {};
  const budget = data?.budget_analysis || {};
  const subscriptions = data?.subscription_analysis || {};

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-6xl mx-auto py-10 px-6">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-semibold text-slate-900">Financial Dashboard</h1>
          <button
            onClick={fetchAnalysis}
            className="text-sm font-medium text-slate-900 border border-slate-300 px-4 py-2 rounded-lg hover:bg-slate-100"
          >
            Refresh Analysis
          </button>
        </div>

        {error && <p className="text-red-600 text-sm mb-6">{error}</p>}

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
          <StatCard label="Total Spent" value={formatCurrency(expense.total_spent)} />
          <StatCard
            label="Financial Health"
            value={`${budget.financial_health_score ?? "—"} / 100`}
            accent={budget.financial_health_score < 60 ? "red" : "emerald"}
          />
          <StatCard label="Active Subscriptions" value={subscriptions.active_count ?? 0} />
          <StatCard
            label="Annual Subscription Cost"
            value={formatCurrency(subscriptions.total_estimated_annual_cost)}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h3 className="font-semibold text-slate-900 mb-4">Expense Distribution</h3>
            <CategoryChart data={expense.category_distribution} />
          </div>
          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h3 className="font-semibold text-slate-900 mb-4">Monthly Trend</h3>
            <TrendChart data={expense.monthly_trend} />
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-6 mb-10">
          <h3 className="font-semibold text-slate-900 mb-4">Budget Performance</h3>
          <BudgetTable variance={budget.variance} />
        </div>

        <div>
          <h3 className="font-semibold text-slate-900 mb-4">Recommendations</h3>
          <RecommendationList recommendations={data?.recommendations} />
        </div>
      </div>
    </div>
  );
}
