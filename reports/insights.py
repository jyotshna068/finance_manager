from typing import Dict, Any, List


def build_executive_summary(state: Dict[str, Any]) -> str:
    """
    Produces a short natural-language executive summary stitched
    together from each agent's analysis — the first thing a user reads.
    """
    expense = state.get("expense_analysis") or {}
    budget = state.get("budget_analysis") or {}
    subscriptions = state.get("subscription_analysis") or {}

    total_spent = expense.get("total_spent", 0)
    health_score = budget.get("financial_health_score", "N/A")
    active_subs = subscriptions.get("active_count", 0)
    annual_sub_cost = subscriptions.get("total_estimated_annual_cost", 0)
    
    summary = (
        f"Total spending analyzed: ₹{total_spent:,.2f} across {expense.get('transaction_count', 0)} transactions. "
        f"Current financial health score: {health_score}/100. "
    )

    if active_subs:
        summary += (
            f"{active_subs} active recurring subscriptions detected, "
            f"costing an estimated ₹{annual_sub_cost:,.2f} annually. "
        )

    overspent_categories = [
        cat for cat, data in budget.get("variance", {}).items() if data.get("overspent")
    ]
    if overspent_categories:
        summary += f"Overspending detected in: {', '.join(overspent_categories)}."

    return summary

def build_recommendation_summary(recommendations: List[Dict[str, Any]]) -> str:
    recommendations = recommendations or []
    if not recommendations:
        return "No specific recommendations at this time — finances appear well-managed."

    top = recommendations[:3]
    lines = [f"- {r['title']}: {r['reasoning']}" for r in top]
    return "Top priorities:\n" + "\n".join(lines)


def build_investment_insight(investment_analysis: Dict[str, Any]) -> str:
    investment_analysis = investment_analysis or {}
    if not investment_analysis:
        return "No investment data available for this period."

    returns = investment_analysis.get("returns", {})
    risk_level = investment_analysis.get("risk_level", "unknown")

    return (
        f"Portfolio return: {returns.get('return_percent', 0)}% "
        f"(₹{returns.get('absolute_return', 0):,.2f} absolute gain/loss). "
        f"Current risk level assessed as {risk_level}."
    )