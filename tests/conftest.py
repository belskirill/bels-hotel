from pathlib import Path
from typing import AsyncGenerator
import aiofiles
from sqlalchemy.ext.asyncio import create_async_engine
import pytest
import json
from httpx import AsyncClient
from httpx import ASGITransport

from src.api.dependencies import DBDep, get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager

current_dir = Path(__file__).parent
file_path = current_dir / "mock_hotels.json"
file_path2 = current_dir / "mock_rooms.json"


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope='function')
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope='session', autouse=True)
async def database_setup(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
        content = await file.read()
        data = json.loads(content)
        add_data_hotels = [HotelAdd.model_validate(item) for item in data]

    async with aiofiles.open(file_path2, mode='r', encoding='utf-8') as file:
        content = await file.read()
        data = json.loads(content)
        add_data_rooms = [RoomsAdd.model_validate(item) for item in data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(add_data_hotels)
        await db_.rooms.add_bulk(add_data_rooms)
        await db_.commit()



@pytest.fixture(scope='session')
async def ac() -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as ac:
        yield ac


@pytest.fixture(scope='session', autouse=True)
async def async_client(ac, database_setup):
        await ac.post(
            '/auth/register',
            json={
                'email': 'kirill666777@test.ru',
                'password': '1234',
            }
        )












