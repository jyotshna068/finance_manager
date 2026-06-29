def _register_and_get_token(client, email="dash@example.com"):
    res = client.post("/auth/register", json={"name": "Dash User", "email": email, "password": "pass1234"})
    return res.json()["access_token"]


def test_dashboard_analysis_with_no_transactions(client):
    token = _register_and_get_token(client)
    res = client.get("/dashboard/analysis", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200
    data = res.json()
    assert data["expense_analysis"]["total_spent"] == 0


def test_dashboard_requires_authentication(client):
    res = client.get("/dashboard/analysis")
    assert res.status_code == 401