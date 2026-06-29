export function formatCurrency(amount, currency = "INR") {
  if (amount === null || amount === undefined) return "—";
  const symbol = currency === "INR" ? "₹" : "$";
  return `${symbol}${Number(amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

export function formatPercent(value) {
  if (value === null || value === undefined) return "—";
  return `${value > 0 ? "+" : ""}${value}%`;
}

export function formatDate(dateStr) {
  if (!dateStr) return "—";
  const date = new Date(dateStr);
  return date.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
}

export function urgencyColor(urgency) {
  switch (urgency) {
    case "high":
      return "text-red-600 bg-red-50";
    case "medium":
      return "text-amber-600 bg-amber-50";
    default:
      return "text-emerald-600 bg-emerald-50";
  }
}
