import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_register_user():
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


@pytest.mark.asyncio
async def test_login_user():
    # 先註冊用戶
    register_response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    assert register_response.status_code == 200
    assert register_response.json() == {"msg": "User registered successfully"}

    # 再進行登入
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpassword"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
