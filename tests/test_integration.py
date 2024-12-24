import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_register_and_login():
    # 註冊用戶
    register_response = client.post(
        "/auth/register",
        json={
            "username": "integration_user",
            "email": "integration@example.com",
            "password": "integrationpass",
        },
    )
    assert register_response.status_code == 200
    assert register_response.json() == {"msg": "User registered successfully"}

    # 登入用戶
    login_response = client.post(
        "/auth/login",
        json={"username": "integration_user", "password": "integrationpass"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    # 驗證 Token
    access_token = login_response.json()["access_token"]
    protected_response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert protected_response.status_code == 200
    assert "Hello, integration@example.com!" in protected_response.json()["message"]
