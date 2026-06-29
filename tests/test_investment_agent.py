from agents.investment_agent import investment_agent_node


def test_computes_returns_correctly():
    state = {
        "investment_accounts": [
            {"sector": "Tech", "asset_type": "stock", "invested_amount": 1000, "current_value": 1200},
            {"sector": "Tech", "asset_type": "stock", "invested_amount": 500, "current_value": 450},
        ]
    }

    result = investment_agent_node(state)
    returns = result["investment_analysis"]["returns"]

    assert returns["total_invested"] == 1500
    assert returns["total_current"] == 1650
    assert returns["absolute_return"] == 150


def test_detects_sector_imbalance():
    state = {
        "investment_accounts": [
            {"sector": "Tech", "asset_type": "stock", "invested_amount": 900, "current_value": 900},
            {"sector": "Gold", "asset_type": "commodity", "invested_amount": 100, "current_value": 100},
        ]
    }

    result = investment_agent_node(state)
    assert "Tech" in result["investment_analysis"]["imbalanced_sectors"]


def test_handles_empty_portfolio():
    state = {"investment_accounts": []}
    result = investment_agent_node(state)
    assert result["investment_analysis"]["returns"]["total_invested"] == 0