import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from typing import AsyncIterator


# from app.database.connection import async_session_maker as SessionLocal
# from app.database.connection import engine as test_engine
# from app.database.base_model import Base
from app.main import app
from app.config import settings

from app.modules.users.dao import UserDAO
from app.modules.users.schemas import SUserUpdate

@pytest_asyncio.fixture()
async def client() -> AsyncIterator[AsyncClient]:
    if settings.MODE != 'TEST':
        raise ValueError(
            "Тестирование необходимо запускать в тестовой среде. "
            "Для запуска тестов введите команду MODE=TEST pytest"
        )
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture()
async def superuser(client: AsyncClient) -> AsyncIterator[dict]:
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
    
    user = await UserDAO.get_object(username="testuser")
    if not user or not (user.is_superuser and user.is_verified):
        await client.post("/auth/register", json=user_data)

        update_data = SUserUpdate(**update_data)
        updated_user = await UserDAO.update_object(update_data, username="testuser")
        assert updated_user.is_superuser == True

    login_data = {
        "username": "test@example.com", 
        "password": "testpass"
    }
    response = await client.post("/auth/jwt/login", data=login_data)
    token = response.cookies.get("marketplace")
    header = {"Cookie": f"marketplace={token}"}
    yield header