def test_register_and_login(client):
    register_payload = {"name": "Test User", "email": "test@example.com", "password": "secret123"}
    res = client.post("/auth/register", json=register_payload)
    assert res.status_code == 200
    assert "access_token" in res.json()

    login_payload = {"email": "test@example.com", "password": "secret123"}
    res = client.post("/auth/login", json=login_payload)
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_fails_with_wrong_password(client):
    client.post("/auth/register", json={"name": "Test", "email": "a@a.com", "password": "right"})
    res = client.post("/auth/login", json={"email": "a@a.com", "password": "wrong"})
    assert res.status_code == 401


def test_duplicate_registration_fails(client):
    payload = {"name": "Test", "email": "dup@example.com", "password": "secret123"}
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 400