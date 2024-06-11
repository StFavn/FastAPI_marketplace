import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator


from app.database.connection import async_session_maker as SessionLocal
from app.database.connection import engine as test_engine
from app.database.base_model import Base
from app.main import app
from app.config import settings

from app.modules.users.dao import UserDAO
from app.modules.users.schemas import SUserUpdate

pytest_plugins = ['pytest_asyncio']

async def superuser(client):
    user_data = {
        "username": "testuser", 
        "first_name": "User",
        "last_name": "Test",
        "email": "test@example.com",
        "password": "testpass"
    }

    update_data = {
        "is_superuser": True,
        "is_verified": True
    }
    update_data = SUserUpdate(**update_data)

    login_data = {
        "username": "test@example.com", 
        "password": "testpass"
    }

    response = await client.post("/auth/register", json=user_data)

    updated_user = await UserDAO.update_object(update_data, username="testuser")
    assert updated_user.is_superuser == True

    response = await client.post("/auth/jwt/login", data=login_data)
    token = response.cookies.get("marketplace")
    header = {"Cookie": f"marketplace={token}"}
    return header

@pytest.fixture(scope="function", autouse=True)
async def client() -> AsyncGenerator[AsyncClient, None]:
    if settings.MODE != 'TEST':
        raise ValueError(
            "Тестирование необходимо запускать в тестовой среде. "
            "Для запуска тестов введите команду MODE=TEST pytest"
        )
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = await superuser(client)
        yield client, headers