def test_register_and_login(client):
    response = client.post(
        "/register",
        data={"username": "vadim", "email": "vadim@example.com", "password": "strong-password", "repeat_password": "strong-password"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert "interviewforge_session" in response.headers["set-cookie"]

    client.post("/logout")
    login = client.post("/login", data={"email": "vadim@example.com", "password": "strong-password"}, follow_redirects=False)
    assert login.status_code == 303


def test_wrong_password(client):
    client.post(
        "/register",
        data={"username": "vadim", "email": "vadim@example.com", "password": "strong-password", "repeat_password": "strong-password"},
    )
    response = client.post("/login", data={"email": "vadim@example.com", "password": "bad"}, follow_redirects=False)
    assert response.status_code == 400


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"

