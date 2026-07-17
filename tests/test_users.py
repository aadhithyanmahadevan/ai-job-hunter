from uuid import uuid4


def register_and_login(client):
    email = f"user_{uuid4().hex[:8]}@example.com"
    password = "Password123!"

    register_payload = {
        "full_name": "Test User",
        "email": email,
        "password": password,
    }

    client.post("/auth/register", json=register_payload)

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    return token, register_payload


def test_get_current_user(client):
    token, user = register_and_login(client)

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == user["email"]
    assert data["full_name"] == user["full_name"]


def test_get_current_user_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_get_current_user_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401
