from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("email,password,status_code", [
    ("kot@example.com", "kotopes", 200),
    ("kot@example.com", "kot0pes", 409),
    ("kotexample.com", "kot0pes", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code

@pytest.mark.parametrize("email,password,status_code", [
    ("test1@example.com", "hashed_pass_1", 200),
    ("test2@example.com", "hashed_pass_2", 200),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code