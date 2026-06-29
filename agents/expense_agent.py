from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any
from workflows.state import FinanceState


def _group_by_category(transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    totals = defaultdict(float)
    for t in transactions:
        category = t.get("category", "uncategorized")
        totals[category] += abs(t.get("amount", 0))
    return dict(totals)


def _monthly_trend(transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    trend = defaultdict(float)
    for t in transactions:
        date = t.get("date")
        if isinstance(date, datetime):
            key = date.strftime("%Y-%m")
            trend[key] += abs(t.get("amount", 0))
    return dict(sorted(trend.items()))


def _detect_outliers(transactions: List[Dict[str, Any]], threshold_multiplier: float = 2.0) -> List[Dict[str, Any]]:
    amounts = [abs(t.get("amount", 0)) for t in transactions]
    if not amounts:
        return []
    avg = sum(amounts) / len(amounts)
    return [t for t in transactions if abs(t.get("amount", 0)) > avg * threshold_multiplier]


def _merchant_frequency(transactions: List[Dict[str, Any]]) -> Dict[str, int]:
    freq = defaultdict(int)
    for t in transactions:
        merchant = t.get("merchant", t.get("description", "unknown"))
        freq[merchant] += 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10])


def expense_agent_node(state: FinanceState) -> FinanceState:
    """
    Performs multidimensional spending analysis: category distribution,
    monthly trends, merchant frequency, and outlier detection.
    """
    transactions = [t for t in state.get("raw_transactions", []) if t.get("transaction_type") == "debit"]

    analysis = {
        "category_distribution": _group_by_category(transactions),
        "monthly_trend": _monthly_trend(transactions),
        "top_merchants": _merchant_frequency(transactions),
        "outliers": _detect_outliers(transactions),
        "total_spent": sum(abs(t.get("amount", 0)) for t in transactions),
        "transaction_count": len(transactions),
    }

    state["expense_analysis"] = analysis
    return state