from datetime import datetime
from agents.expense_agent import expense_agent_node


def test_expense_agent_categorizes_and_sums():
    state = {
        "raw_transactions": [
            {"amount": -500, "transaction_type": "debit", "category": "food", "date": datetime(2026, 6, 1)},
            {"amount": -300, "transaction_type": "debit", "category": "food", "date": datetime(2026, 6, 5)},
            {"amount": -1000, "transaction_type": "debit", "category": "shopping", "date": datetime(2026, 6, 10)},
        ]
    }

    result = expense_agent_node(state)
    analysis = result["expense_analysis"]

    assert analysis["category_distribution"]["food"] == 800
    assert analysis["category_distribution"]["shopping"] == 1000
    assert analysis["total_spent"] == 1800
    assert analysis["transaction_count"] == 3


def test_expense_agent_detects_outliers():
    state = {
        "raw_transactions": [
            {"amount": -100, "transaction_type": "debit", "category": "food", "date": datetime(2026, 6, 1)},
            {"amount": -100, "transaction_type": "debit", "category": "food", "date": datetime(2026, 6, 2)},
            {"amount": -5000, "transaction_type": "debit", "category": "food", "date": datetime(2026, 6, 3)},
        ]
    }

    result = expense_agent_node(state)
    outliers = result["expense_analysis"]["outliers"]
    assert len(outliers) == 1
    assert outliers[0]["amount"] == -5000


def test_expense_agent_handles_empty_transactions():
    state = {"raw_transactions": []}
    result = expense_agent_node(state)
    assert result["expense_analysis"]["total_spent"] == 0
    assert result["expense_analysis"]["transaction_count"] == 0