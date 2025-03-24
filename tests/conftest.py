from pathlib import Path
from typing import AsyncGenerator
import aiofiles
from sqlalchemy.ext.asyncio import create_async_engine
import pytest
import json
from httpx import AsyncClient
from httpx import ASGITransport

from src.api.dependencies import DBDep
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

@pytest.fixture(scope='session', autouse=True)
async def database_setup():
    assert settings.MODE == 'TEST'
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
        content = await file.read()
        data = json.loads(content)
        add_data_hotels = [HotelAdd(**item) for item in data]

    async with aiofiles.open(file_path2, mode='r', encoding='utf-8') as file:
        content = await file.read()
        data = json.loads(content)
        add_data_rooms = [RoomsAdd(**item) for item in data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(add_data_hotels)
        await db.rooms.add_bulk(add_data_rooms)


        await db.commit()






@pytest.fixture(scope='session', autouse=True)
async def async_client(database_setup):
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url='http://test'
    ) as ac:
        await ac.post(
            '/auth/register',
            json={
                'email': 'kirill666777@test.ru',
                'password': '1234',
            }
        )











