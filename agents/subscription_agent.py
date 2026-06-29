from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any
from workflows.state import FinanceState


def _group_by_merchant(transactions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped = defaultdict(list)
    for t in transactions:
        merchant = t.get("merchant", t.get("description", "unknown"))
        grouped[merchant].append(t)
    return grouped


def _detect_billing_interval(dates: List[datetime]) -> str:
    """Estimates billing cycle based on average gap between charges."""
    if len(dates) < 2:
        return "unknown"

    sorted_dates = sorted(dates)
    gaps = [(sorted_dates[i + 1] - sorted_dates[i]).days for i in range(len(sorted_dates) - 1)]
    avg_gap = sum(gaps) / len(gaps)

    if 25 <= avg_gap <= 35:
        return "monthly"
    elif 6 <= avg_gap <= 8:
        return "weekly"
    elif 350 <= avg_gap <= 380:
        return "yearly"
    return "irregular"


def _is_inactive(last_date: datetime, reference_date: datetime, billing_interval: str) -> bool:
    """Flags a subscription inactive if no charge occurred for 2x its expected interval."""
    interval_days = {"monthly": 30, "weekly": 7, "yearly": 365}.get(billing_interval, 60)
    return (reference_date - last_date).days > (interval_days * 2)


def subscription_agent_node(state: FinanceState) -> FinanceState:
    """
    Identifies recurring payments by grouping transactions per merchant
    and analyzing billing intervals, rather than relying on exact
    string matches — making it robust to minor description variations.
    """
    transactions = [t for t in state.get("raw_transactions", []) if t.get("transaction_type") == "debit"]
    grouped = _group_by_merchant(transactions)

    subscriptions = []
    reference_date = datetime.utcnow()

    for merchant, txns in grouped.items():
        if len(txns) < 2:
            continue  # need at least 2 occurrences to call it recurring

        dates = [t["date"] for t in txns if t.get("date")]
        amounts = [t.get("amount", 0) for t in txns]

        billing_interval = _detect_billing_interval(dates)
        if billing_interval == "irregular" or billing_interval == "unknown":
            continue

        last_date = max(dates)
        avg_amount = sum(amounts) / len(amounts)
        amount_variance = max(amounts) - min(amounts)
        price_increased = amount_variance > (avg_amount * 0.1)

        annual_cost = avg_amount * {"monthly": 12, "weekly": 52, "yearly": 1}.get(billing_interval, 12)

        subscriptions.append({
            "merchant": merchant,
            "billing_interval": billing_interval,
            "average_amount": round(avg_amount, 2),
            "last_billed": last_date,
            "is_active": not _is_inactive(last_date, reference_date, billing_interval),
            "price_increase_detected": price_increased,
            "estimated_annual_cost": round(annual_cost, 2),
            "occurrence_count": len(txns),
        })

    total_annual_cost = sum(s["estimated_annual_cost"] for s in subscriptions if s["is_active"])
    inactive_subs = [s for s in subscriptions if not s["is_active"]]

    state["subscription_analysis"] = {
        "subscriptions": subscriptions,
        "active_count": len([s for s in subscriptions if s["is_active"]]),
        "inactive_subscriptions": inactive_subs,
        "total_estimated_annual_cost": round(total_annual_cost, 2),
    }

    return state