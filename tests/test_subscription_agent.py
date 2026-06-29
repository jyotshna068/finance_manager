from datetime import datetime
from agents.subscription_agent import subscription_agent_node


def test_detects_monthly_subscription():
    state = {
        "raw_transactions": [
            {"merchant": "Netflix", "amount": -500, "transaction_type": "debit", "date": datetime(2026, 4, 1)},
            {"merchant": "Netflix", "amount": -500, "transaction_type": "debit", "date": datetime(2026, 5, 1)},
            {"merchant": "Netflix", "amount": -500, "transaction_type": "debit", "date": datetime(2026, 6, 1)},
        ]
    }

    result = subscription_agent_node(state)
    subs = result["subscription_analysis"]["subscriptions"]

    assert len(subs) == 1
    assert subs[0]["billing_interval"] == "monthly"
    assert subs[0]["merchant"] == "Netflix"


def test_ignores_single_occurrence_merchant():
    state = {
        "raw_transactions": [
            {"merchant": "OneTimeStore", "amount": -200, "transaction_type": "debit", "date": datetime(2026, 6, 1)},
        ]
    }
    result = subscription_agent_node(state)
    assert result["subscription_analysis"]["subscriptions"] == []


def test_detects_price_increase():
    state = {
        "raw_transactions": [
            {"merchant": "Spotify", "amount": -120, "transaction_type": "debit", "date": datetime(2026, 4, 1)},
            {"merchant": "Spotify", "amount": -120, "transaction_type": "debit", "date": datetime(2026, 5, 1)},
            {"merchant": "Spotify", "amount": -180, "transaction_type": "debit", "date": datetime(2026, 6, 1)},
        ]
    }
    result = subscription_agent_node(state)
    subs = result["subscription_analysis"]["subscriptions"]
    assert subs[0]["price_increase_detected"] is True