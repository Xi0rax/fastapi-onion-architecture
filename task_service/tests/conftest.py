"""Contains helper fixtures for setup tests infrastructure."""

import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy
from httpx import AsyncClient
from sqlalchemy import Result, sql
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.config import settings
from src.main import app
from src.models import BaseModel
from src.utils.unit_of_work import UnitOfWork
from tests.fixtures.db_mocks.mock_uow import get_mock_uow


@pytest.fixture(scope='session')
def event_loop() -> asyncio.AbstractEventLoop:
    """Returns a new event loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def fake_uow():
    """Returns an in-memory mocked UnitOfWork for service and API tests."""
    return get_mock_uow()


@pytest_asyncio.fixture
async def client(fake_uow) -> AsyncGenerator[AsyncClient, None]:
    """Returns async test client with UnitOfWork overridden."""
    app.dependency_overrides[UnitOfWork] = lambda: fake_uow
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def db_tests_enabled() -> bool:
    return os.getenv('RUN_DB_TESTS') == '1'


@pytest_asyncio.fixture(scope='session')
async def create_test_db(db_tests_enabled: bool) -> AsyncGenerator[None, None]:
    """Creates a PostgreSQL test database only when RUN_DB_TESTS=1."""
    if not db_tests_enabled:
        yield
        return

    assert settings.MODE == 'TEST'

    sqlalchemy_database_url = (
        f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}'
        f'@{settings.DB_HOST}:{settings.DB_PORT}/'
    )
    nodb_engine = create_async_engine(
        sqlalchemy_database_url,
        echo=False,
        future=True,
    )
    db = AsyncSession(bind=nodb_engine)

    db_exists_query = sql.text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.DB_NAME}'")
    db_exists: Result = await db.execute(db_exists_query)
    db_exists = db_exists.fetchone() is not None
    autocommit_engine = nodb_engine.execution_options(isolation_level='AUTOCOMMIT')
    connection = await autocommit_engine.connect()
    if not db_exists:
        await connection.execute(sql.text(f'CREATE DATABASE {settings.DB_NAME}'))

    yield

    await db.close()
    await connection.execute(sql.text(f'DROP DATABASE IF EXISTS {settings.DB_NAME} WITH (FORCE)'))
    await connection.close()
    await nodb_engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def db_engine(create_test_db: None, db_tests_enabled: bool) -> AsyncGenerator[AsyncEngine | None, None]:
    """Returns the test engine when DB integration tests are enabled."""
    if not db_tests_enabled:
        yield None
        return

    engine = create_async_engine(
        settings.DB_URL,
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
    ).execution_options(compiled_cache=None)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(db_engine: AsyncEngine | None) -> None:
    """Creates tables in the test database."""
    if db_engine is None:
        return

    assert settings.MODE == 'TEST'
    async with db_engine.begin() as db_conn:
        await db_conn.run_sync(BaseModel.metadata.drop_all)
        await db_conn.run_sync(BaseModel.metadata.create_all)


@pytest_asyncio.fixture
async def async_session(db_engine: AsyncEngine | None) -> AsyncGenerator[AsyncSession, None]:
    """Returns a rollbacked DB session for repository integration tests."""
    if db_engine is None:
        pytest.skip('Repository integration tests require RUN_DB_TESTS=1')

    connection = await db_engine.connect()
    await connection.begin()
    session = AsyncSession(bind=connection)

    yield session

    await session.rollback()
    await connection.close()
