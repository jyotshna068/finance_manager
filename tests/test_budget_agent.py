from agents.budget_agent import budget_agent_node


def test_budget_agent_computes_variance():
    state = {
        "expense_analysis": {"category_distribution": {"food": 1200}},
        "has_budget_data": True,
        "budgets": {"food": 1000},
    }

    result = budget_agent_node(state)
    variance = result["budget_analysis"]["variance"]["food"]

    assert variance["overspent"] is True
    assert variance["variance_amount"] == 200
    assert round(variance["variance_percent"], 2) == 20.0


def test_budget_agent_auto_generates_when_missing():
    state = {
        "expense_analysis": {"category_distribution": {"travel": 1000}},
        "has_budget_data": False,
        "budgets": None,
    }

    result = budget_agent_node(state)
    assert result["budget_analysis"]["auto_generated"] is True
    assert result["budget_analysis"]["planned_budget"]["travel"] == 1100  # +10% buffer


def test_financial_health_score_drops_with_overspending():
    state = {
        "expense_analysis": {"category_distribution": {"food": 2000}},
        "has_budget_data": True,
        "budgets": {"food": 1000},
    }
    result = budget_agent_node(state)
    assert result["budget_analysis"]["financial_health_score"] < 100