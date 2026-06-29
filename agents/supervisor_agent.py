from workflows.state import FinanceState


def supervisor_node(state: FinanceState) -> FinanceState:
    """
    Entry node of the workflow. Validates incoming state, sets routing
    flags based on data availability, and initializes error tracking.
    """
    errors = state.get("errors", [])

    transactions = state.get("raw_transactions", [])
    if not transactions:
        errors.append("No transactions found for this user.")

    # Determine which optional agents should run
    has_investment_data = any(
        t.get("category") == "investment" for t in transactions
    ) or bool(state.get("investment_accounts"))

    has_subscription_data = any(
        t.get("is_recurring") for t in transactions
    )

    has_budget_data = bool(state.get("budgets"))

    state["has_investment_data"] = has_investment_data
    state["has_subscription_data"] = has_subscription_data
    state["has_budget_data"] = has_budget_data
    state["errors"] = errors

    return state