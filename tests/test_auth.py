from uuid import uuid4


def unique_email():
    return f"test_{uuid4().hex[:8]}@example.com"


def test_register_user(client):
    payload = {
        "full_name": "Test User",
        "email": unique_email(),
        "password": "Password123!",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert "id" in data


def test_duplicate_registration(client):
    email = unique_email()

    payload = {"full_name": "Test User", "email": email, "password": "Password123!"}

    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success(client):
    email = unique_email()

    register_payload = {
        "full_name": "Login User",
        "email": email,
        "password": "Password123!",
    }

    client.post("/auth/register", json=register_payload)

    login_payload = {"username": email, "password": "Password123!"}

    response = client.post(
        "/auth/login",
        data=login_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    email = unique_email()

    register_payload = {
        "full_name": "Wrong Password",
        "email": email,
        "password": "Password123!",
    }

    client.post("/auth/register", json=register_payload)

    response = client.post(
        "/auth/login",
        data={"username": email, "password": "WrongPassword"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
