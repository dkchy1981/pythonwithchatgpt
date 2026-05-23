from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_success():
    response = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_invalid_credentials():
    response = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_unknown_user():
    response = client.post("/login", json={"username": "unknown", "password": "admin123"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_userdetails_missing_authorization_header():
    response = client.get("/userdetails")
    assert response.status_code == 401
    assert response.json() == {"detail": "Authorization header missing"}


def test_userdetails_invalid_token_format():
    response = client.get("/userdetails", headers={"Authorization": "Token basic-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_userdetails_invalid_token_value():
    response = client.get("/userdetails", headers={"Authorization": "Bearer wrong-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_userdetails_bearer_without_token_value():
    response = client.get("/userdetails", headers={"Authorization": "Bearer"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_userdetails_expired_token():
    login_response = client.post("/login", json={"username": "admin", "password": "admin123"})
    token = login_response.json()["access_token"]
    with patch("app.main.time.time", return_value=10**10):
        response = client.get("/userdetails", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_userdetails_success():
    login_response = client.post("/login", json={"username": "admin", "password": "admin123"})
    token = login_response.json()["access_token"]
    response = client.get("/userdetails", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"username": "admin", "email": "admin@example.com"}


def test_swagger_endpoint_is_available():
    response = client.get("/docs")
    assert response.status_code == 200
