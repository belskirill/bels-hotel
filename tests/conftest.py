from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
import pytest

from httpx import AsyncClient
from httpx import ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope='session', autouse=True)
async def database_setup():
    assert settings.MODE == 'TEST'
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)




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









