from langgraph.graph import StateGraph, END
from workflows.state import FinanceState

from agents.supervisor_agent import supervisor_node
from agents.expense_agent import expense_agent_node
from agents.budget_agent import budget_agent_node
from agents.investment_agent import investment_agent_node
from agents.subscription_agent import subscription_agent_node
from agents.recommendation_agent import recommendation_agent_node

from reports.pdf_generator import generate_report_node


def route_after_validation(state: FinanceState) -> str:
    """Entry routing — always goes to expense agent first."""
    return "expense_agent"


def route_after_expense(state: FinanceState) -> str:
    """Budget analysis always runs; missing budgets are auto-generated downstream."""
    return "budget_agent"


def route_after_budget(state: FinanceState) -> str:
    """Skip investment agent if user has no investment data."""
    if state.get("has_investment_data"):
        return "investment_agent"
    return "subscription_router"


def route_after_investment(state: FinanceState) -> str:
    return "subscription_router"


def route_subscription(state: FinanceState) -> str:
    """Skip subscription agent if no recurring-payment data exists."""
    if state.get("has_subscription_data"):
        return "subscription_agent"
    return "recommendation_agent"


def route_after_subscription(state: FinanceState) -> str:
    return "recommendation_agent"


def build_finance_graph():
    """
    Builds and compiles the LangGraph state machine that drives the
    entire financial reasoning workflow, with conditional routing
    around optional data sources (investments, subscriptions).
    """
    graph = StateGraph(FinanceState)

    # Register nodes
    graph.add_node("data_validation", supervisor_node)
    graph.add_node("expense_agent", expense_agent_node)
    graph.add_node("budget_agent", budget_agent_node)
    graph.add_node("investment_agent", investment_agent_node)
    graph.add_node("subscription_agent", subscription_agent_node)
    graph.add_node("recommendation_agent", recommendation_agent_node)
    graph.add_node("report_generator", generate_report_node)

    # Entry point
    graph.set_entry_point("data_validation")

    # Conditional edges
    graph.add_conditional_edges(
        "data_validation", route_after_validation, {"expense_agent": "expense_agent"}
    )
    graph.add_conditional_edges(
        "expense_agent", route_after_expense, {"budget_agent": "budget_agent"}
    )
    graph.add_conditional_edges(
        "budget_agent",
        route_after_budget,
        {
            "investment_agent": "investment_agent",
            "subscription_router": "subscription_agent_router_placeholder",
        },
    )

    # Investment -> subscription routing
    graph.add_conditional_edges(
        "investment_agent",
        route_after_investment,
        {"subscription_router": "subscription_agent_router_placeholder"},
    )

    # Because LangGraph conditional edges need real nodes, we use a
    # lightweight pass-through node to decide on subscription_agent vs skip
    graph.add_node("subscription_agent_router_placeholder", lambda state: state)

    graph.add_conditional_edges(
        "subscription_agent_router_placeholder",
        route_subscription,
        {
            "subscription_agent": "subscription_agent",
            "recommendation_agent": "recommendation_agent",
        },
    )

    graph.add_conditional_edges(
        "subscription_agent",
        route_after_subscription,
        {"recommendation_agent": "recommendation_agent"},
    )

    graph.add_edge("recommendation_agent", "report_generator")
    graph.add_edge("report_generator", END)

    return graph.compile()


# Singleton compiled graph used by API layer
finance_graph = build_finance_graph()