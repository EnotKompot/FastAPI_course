import pytest
from httpx import AsyncClient, ASGITransport

from config import settings
from src.main import app
from src.utils.database import BaseModel, engine_null_pool
from src.models import *



@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def test_register_user():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.ru",
                "nickname": "kot",
                "password": "password12345",
            }
        )

    assert response.json() == {"success": True}