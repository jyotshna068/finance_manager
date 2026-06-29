from collections import defaultdict
from typing import List, Dict, Any
from workflows.state import FinanceState


def _sector_allocation(investments: List[Dict[str, Any]]) -> Dict[str, float]:
    totals = defaultdict(float)
    for inv in investments:
        sector = inv.get("sector", "unclassified")
        totals[sector] += inv.get("current_value", 0)
    return dict(totals)


def _asset_type_allocation(investments: List[Dict[str, Any]]) -> Dict[str, float]:
    totals = defaultdict(float)
    for inv in investments:
        asset_type = inv.get("asset_type", "unknown")
        totals[asset_type] += inv.get("current_value", 0)
    return dict(totals)


def _compute_returns(investments: List[Dict[str, Any]]) -> Dict[str, float]:
    total_invested = sum(inv.get("invested_amount", 0) for inv in investments)
    total_current = sum(inv.get("current_value", 0) for inv in investments)

    if total_invested == 0:
        return {"total_invested": 0, "total_current": 0, "absolute_return": 0, "return_percent": 0}

    absolute_return = total_current - total_invested
    return_percent = (absolute_return / total_invested) * 100

    return {
        "total_invested": round(total_invested, 2),
        "total_current": round(total_current, 2),
        "absolute_return": round(absolute_return, 2),
        "return_percent": round(return_percent, 2),
    }


def _diversification_score(sector_allocation: Dict[str, float]) -> float:
    """
    Heuristic: penalizes concentration. If one sector holds >50% of
    portfolio value, diversification score drops sharply.
    """
    total = sum(sector_allocation.values())
    if total == 0:
        return 0.0

    max_share = max(sector_allocation.values()) / total
    score = max(100 - (max_share * 100), 0)
    return round(score, 2)


def _detect_imbalance(sector_allocation: Dict[str, float], threshold: float = 0.5) -> List[str]:
    total = sum(sector_allocation.values())
    if total == 0:
        return []
    return [sector for sector, value in sector_allocation.items() if (value / total) > threshold]


def investment_agent_node(state: FinanceState) -> FinanceState:
    """
    Analyzes portfolio diversification, sector/asset allocation,
    returns, and imbalance risk. Skipped entirely if no investment
    data exists (handled by graph routing).
    """
    investments = state.get("investment_accounts", [])

    sector_allocation = _sector_allocation(investments)
    asset_allocation = _asset_type_allocation(investments)
    returns = _compute_returns(investments)
    diversification_score = _diversification_score(sector_allocation)
    imbalanced_sectors = _detect_imbalance(sector_allocation)

    state["investment_analysis"] = {
        "sector_allocation": sector_allocation,
        "asset_allocation": asset_allocation,
        "returns": returns,
        "diversification_score": diversification_score,
        "imbalanced_sectors": imbalanced_sectors,
        "risk_level": "high" if diversification_score < 40 else "moderate" if diversification_score < 70 else "low",
    }

    return state