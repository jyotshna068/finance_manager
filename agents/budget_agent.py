from typing import Dict, Any
from workflows.state import FinanceState


def _auto_generate_budget(category_spend: Dict[str, float]) -> Dict[str, float]:
    """
    Fallback when no user-defined budget exists: generates a naive
    budget by adding a 10% buffer to historical average spend per category.
    """
    return {category: round(amount * 1.10, 2) for category, amount in category_spend.items()}


def _compute_variance(planned: Dict[str, float], actual: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    variance = {}
    categories = set(planned.keys()) | set(actual.keys())
    for category in categories:
        plan_amt = planned.get(category, 0)
        actual_amt = actual.get(category, 0)
        diff = actual_amt - plan_amt
        pct = (diff / plan_amt * 100) if plan_amt else 0
        variance[category] = {
            "planned": plan_amt,
            "actual": actual_amt,
            "variance_amount": round(diff, 2),
            "variance_percent": round(pct, 2),
            "overspent": diff > 0,
        }
    return variance


def _financial_health_score(variance: Dict[str, Dict[str, float]]) -> float:
    """
    Simple scoring heuristic: starts at 100, deducts points for each
    overspent category proportional to severity. Floors at 0.
    """
    score = 100.0
    for data in variance.values():
        if data["overspent"]:
            score -= min(data["variance_percent"] / 2, 15)
    return max(round(score, 2), 0)


def budget_agent_node(state: FinanceState) -> FinanceState:
    """
    Compares planned budgets to actual spend. If no budget exists,
    auto-generates one from historical spending patterns.
    """
    expense_analysis = state.get("expense_analysis", {})
    category_spend = expense_analysis.get("category_distribution", {})

    user_budgets = state.get("budgets")  # expected as {category: planned_amount}

    if not state.get("has_budget_data") or not user_budgets:
        planned = _auto_generate_budget(category_spend)
        auto_generated = True
    else:
        planned = user_budgets
        auto_generated = False

    variance = _compute_variance(planned, category_spend)
    health_score = _financial_health_score(variance)

    state["budget_analysis"] = {
        "planned_budget": planned,
        "auto_generated": auto_generated,
        "variance": variance,
        "financial_health_score": health_score,
    }

    return state