from agents.recommendation_agent import recommendation_agent_node


def test_generates_overspending_recommendation():
    state = {
        "budget_analysis": {
            "variance": {
                "food": {"planned": 1000, "actual": 1500, "variance_amount": 500, "variance_percent": 50, "overspent": True}
            }
        }
    }

    result = recommendation_agent_node(state)
    recs = result["recommendations"]

    assert len(recs) == 1
    assert "food" in recs[0]["title"].lower()
    assert recs[0]["urgency"] == "high"


def test_recommendations_sorted_by_impact():
    state = {
        "budget_analysis": {
            "variance": {
                "food": {"planned": 1000, "actual": 1200, "variance_amount": 200, "variance_percent": 20, "overspent": True},
                "shopping": {"planned": 1000, "actual": 1800, "variance_amount": 800, "variance_percent": 80, "overspent": True},
            }
        }
    }

    result = recommendation_agent_node(state)
    recs = result["recommendations"]
    assert recs[0]["impact_score"] >= recs[1]["impact_score"]


def test_no_recommendations_when_no_issues():
    state = {"budget_analysis": {"variance": {}}}
    result = recommendation_agent_node(state)
    assert result["recommendations"] == []