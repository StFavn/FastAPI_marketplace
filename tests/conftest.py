import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from app.database.connection import async_session_maker as TestSessionLocal
from app.database.connection import engine as test_engine
from app.database.base_model import Base
from app.main import app
from app.config import settings

pytest_plugins = ['pytest_asyncio']

@pytest.fixture(scope="function", autouse=True)
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def client() -> AsyncGenerator[AsyncClient, None]:
    if settings.MODE != 'TEST':
        raise ValueError(
            "Тестирование необходимо запускать в тестовой среде. "
            "Для запуска тестов введите команду MODE=TEST pytest"
        )
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# @pytest.fixture(scope="function", autouse=True)
# async def superuser_headers(client):
#     async for client_instance in client:
#         register_response = await client_instance.post("/auth/register", json={
#             "username": "superuser",
#             "first_name": "Super",
#             "last_name": "User",
#             "email": "superuser@example.com",
#             "password": "password",
#             "is_active": True,
#             "is_superuser": True,
#             "is_verified": True 
#         })
        
#         login_response = await client_instance.post("/auth/jwt/login", data={
#             "username": "superuser@example.com",
#             "password": "password",
#         })

#         # Получение токена из cookies
#         token = login_response.cookies["access_token"]
#         headers = {"Authorization": f"Bearer {token}"}
#         return headers 
