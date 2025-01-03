import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser1",
            "email": "test1@example.com",
            "password": "testpassword1",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "User registered successfully"}


def test_login_user():
    # 再進行登入
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
