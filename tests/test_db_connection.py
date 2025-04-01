from unittest.mock import AsyncMock, patch

import pytest

from app.db.connection import BaseDBConnection, \
    PostgresDBConnection, MySQLDBConnection, get_db_connection


@pytest.mark.asyncio
async def test_base_db_connection():
    db = BaseDBConnection()

    with pytest.raises(NotImplementedError):
        await db.connect()

    with pytest.raises(NotImplementedError):
        await db.disconnect()

    with pytest.raises(NotImplementedError):
        await db.execute_query("SELECT 1")


@pytest.mark.asyncio
@patch("asyncpg.create_pool", new_callable=AsyncMock)
async def test_postgres_connection(mock_create_pool):
    config = {
        'user': 'user',
        'password': 'pass',
        'host': 'localhost',
        'port': '5432',
        'database': 'testdb'
    }
    mock_pool = AsyncMock()
    mock_create_pool.return_value = mock_pool

    db = PostgresDBConnection(config)
    await db.connect()
    assert db.pool == mock_pool

    await db.disconnect()
    mock_pool.close.assert_called_once()


@pytest.mark.asyncio
@patch("aiomysql.create_pool", new_callable=AsyncMock)
async def test_mysql_connection(mock_create_pool):
    config = {
        "user": "user",
        "password": "pass",
        "host": "localhost",
        "port": "3306",
        "database": "testdb"
    }
    mock_pool = AsyncMock()
    mock_create_pool.return_value = mock_pool

    db = MySQLDBConnection(config)
    await db.connect()
    assert db.pool == mock_pool

    await db.disconnect()
    mock_pool.wait_closed.assert_called_once()


@pytest.mark.parametrize("engine, expected_class", [
    ("postgres", PostgresDBConnection),
    ("mysql", MySQLDBConnection)
])
def test_get_db_connection(engine, expected_class):
    config = {
        'engine': engine,
        'user': 'user',
        'password': 'pass',
        'host': 'localhost',
        'port': '5432',
        'database': 'testdb'
    }
    db_instance = get_db_connection(config)
    assert isinstance(db_instance, expected_class)


def test_get_db_connection_invalid():
    config = {"engine": "sqlite"}
    with pytest.raises(ValueError):
        get_db_connection(config)
