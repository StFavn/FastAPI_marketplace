import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from app.database.connection import async_session_maker as TestSessionLocal
from app.database.connection import engine as test_engine
from app.database.base_model import Base
from app.main import app
from app.config import settings

pytest_plugins = ['pytest_asyncio']

@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient, None]:
    if settings.MODE != 'TEST':
        raise ValueError(
            "Тестирование необходимо запускать в тестовой среде. "
            "Для запуска тестов введите команду MODE=TEST pytest"
        )
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module")
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)

