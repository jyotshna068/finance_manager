import { urgencyColor } from "../utils/formatters";

export default function RecommendationList({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <p className="text-sm text-slate-400">
        No recommendations yet — upload a statement and run analysis first.
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {recommendations.map((rec, idx) => (
        <div key={idx} className="rounded-lg border border-slate-200 p-4 bg-white">
          <div className="flex items-start justify-between gap-3">
            <h4 className="font-semibold text-slate-900">{rec.title}</h4>
            <span className={`text-xs font-medium px-2 py-1 rounded-full ${urgencyColor(rec.urgency)}`}>
              {rec.urgency}
            </span>
          </div>
          <p className="text-sm text-slate-600 mt-2">{rec.reasoning}</p>
        </div>
      ))}
    </div>
  );
}
