# ruff: noqa: E402
import json
from unittest import mock


mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.utils.database import BaseModel, engine, new_session
from src.models import *  # noqa
from src.main import app
from src.utils.db_manager import DBManager
from src.schemas.rooms import RoomAddSchema
from src.schemas.hotels import HotelAddSchema


@pytest.fixture(scope="session")
async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=new_session) as db:
        yield db


@pytest.fixture(scope="session")
async def db() -> DBManager:
    async with DBManager(session_factory=new_session) as db:
        yield db


# app.dependency_overrides[get_db()] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(ac, setup_database):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.ru",
            "nickname": "kot",
            "password": "password12345",
        },
    )

    assert response.json() == {"success": True}


@pytest.fixture(scope="session")
async def authenticated_ac(ac, test_register_user):
    await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.ru",
            "nickname": "kot",
            "password": "password12345",
        },
    )
    assert ac.cookies["access_token"] is not None
    yield ac


@pytest.fixture(scope="session", autouse=True)
async def test_add_hotels_mock_data(setup_database, db):
    current_dir = Path(__file__).parent
    file_path = current_dir / "mock_hotels.json"
    with open(file_path, "r", encoding="utf-8") as mock_data:
        hotels_data = json.load(mock_data)

    for hotel in hotels_data:
        await db.hotels.add(HotelAddSchema.model_validate(hotel))
    await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def test_add_rooms_mock_data(test_add_hotels_mock_data, db):
    current_dir = Path(__file__).parent
    file_path = current_dir / "mock_rooms.json"
    with open(file_path, "r", encoding="utf-8") as mock_data:
        rooms_data = json.load(mock_data)

    for room in rooms_data:
        await db.rooms.add(RoomAddSchema.model_validate(room))
    await db.commit()
