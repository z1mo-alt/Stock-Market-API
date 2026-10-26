import os

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from core.database import Base, get_session
from main import app

engine = create_async_engine(os.environ["TEST_DATABASE_URL"], poolclass=NullPool)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def override_get_session():
    async with session_factory() as session:
        yield session


@pytest.fixture
async def client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)