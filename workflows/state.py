from typing import TypedDict, List, Dict, Any, Optional


class FinanceState(TypedDict, total=False):
    """
    Shared state object passed between all LangGraph nodes/agents.
    Each agent reads what it needs and writes its own results back.
    """

    user_id: int
    raw_transactions: List[Dict[str, Any]]

    # Per-agent outputs
    expense_analysis: Optional[Dict[str, Any]]
    budget_analysis: Optional[Dict[str, Any]]
    investment_analysis: Optional[Dict[str, Any]]
    subscription_analysis: Optional[Dict[str, Any]]
    recommendations: Optional[List[Dict[str, Any]]]

    # Flags for conditional routing
    has_investment_data: bool
    has_subscription_data: bool
    has_budget_data: bool

    # Final output
    report_path: Optional[str]
    errors: List[str]