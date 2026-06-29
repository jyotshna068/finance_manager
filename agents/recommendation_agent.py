from typing import List, Dict, Any
from workflows.state import FinanceState


def _budget_recommendations(budget_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    recs = []
    for category, data in budget_analysis.get("variance", {}).items():
        if data.get("overspent") and data["variance_percent"] > 15:
            recs.append({
                "title": f"Reduce {category} spending",
                "reasoning": (
                    f"{category.capitalize()} spending exceeded the planned budget by "
                    f"{data['variance_percent']}% (₹{data['variance_amount']} over plan)."
                ),
                "impact_score": min(data["variance_percent"], 100),
                "urgency": "high" if data["variance_percent"] > 30 else "medium",
            })
    return recs


def _subscription_recommendations(subscription_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    recs = []
    for sub in subscription_analysis.get("inactive_subscriptions", []):
        recs.append({
            "title": f"Cancel unused subscription: {sub['merchant']}",
            "reasoning": (
                f"No charges detected from {sub['merchant']} recently despite an "
                f"active {sub['billing_interval']} billing pattern — likely inactive or forgotten."
            ),
            "impact_score": min(sub["estimated_annual_cost"] / 100, 100),
            "urgency": "low",
        })

    for sub in subscription_analysis.get("subscriptions", []):
        if sub.get("price_increase_detected") and sub["is_active"]:
            recs.append({
                "title": f"Review price increase: {sub['merchant']}",
                "reasoning": (
                    f"{sub['merchant']} billing amount has varied significantly across charges, "
                    f"suggesting a possible price increase."
                ),
                "impact_score": 40,
                "urgency": "medium",
            })

    return recs


def _investment_recommendations(investment_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    recs = []
    if investment_analysis.get("imbalanced_sectors"):
        sectors = ", ".join(investment_analysis["imbalanced_sectors"])
        recs.append({
            "title": "Rebalance portfolio allocation",
            "reasoning": (
                f"Portfolio is heavily concentrated in: {sectors}. "
                f"Diversification score is {investment_analysis.get('diversification_score')}/100, "
                f"indicating elevated concentration risk."
            ),
            "impact_score": 70,
            "urgency": "medium",
        })
    return recs


def recommendation_agent_node(state: FinanceState) -> FinanceState:
    """
    Synthesizes outputs from all prior agents into prioritized,
    explainable recommendations with reasoning traces.
    """
    recommendations: List[Dict[str, Any]] = []

    if state.get("budget_analysis"):
        recommendations.extend(_budget_recommendations(state["budget_analysis"]))

    if state.get("subscription_analysis"):
        recommendations.extend(_subscription_recommendations(state["subscription_analysis"]))

    if state.get("investment_analysis"):
        recommendations.extend(_investment_recommendations(state["investment_analysis"]))

    # Sort by impact score, descending — highest impact recommendations first
    recommendations.sort(key=lambda r: r.get("impact_score", 0), reverse=True)

    state["recommendations"] = recommendations
    return state