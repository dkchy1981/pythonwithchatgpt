from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_success():
    response = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert response.json() == {"access_token": "basic-token", "token_type": "bearer"}


def test_login_invalid_credentials():
    response = client.post("/login", json={"username": "admin", "password": "wrong"})
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


def test_userdetails_success():
    response = client.get("/userdetails", headers={"Authorization": "Bearer basic-token"})
    assert response.status_code == 200
    assert response.json() == {"username": "admin", "email": "admin@example.com"}


def test_swagger_endpoint_is_available():
    response = client.get("/docs")
    assert response.status_code == 200
