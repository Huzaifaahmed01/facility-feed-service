import logging
from typing import Any, Dict, List

import asyncio
import asyncpg
import aiomysql

logger = logging.getLogger(__name__)


class BaseDBConnection:
    """Base class for database connections."""

    async def connect(self):
        """
        Establish a connection to the database.
        :return: Connection object.
        """
        raise NotImplementedError

    async def disconnect(self):
        """"
        Close the connection to the database."
        """
        raise NotImplementedError

    async def execute_query(self, query: str, *params: Any) -> List[Any]:
        """"
        Execute a query on the database.
        :param query: SQL query string.
        :param params: Parameters for the query.
        :return: Result of the query execution.
        """
        raise NotImplementedError


class PostgresDBConnection(BaseDBConnection):
    """
    PostgreSQL database connection class.
    This class manages the connection pool and provides methods to connect,
    disconnect, and execute queries.

    Attributes:
        config (dict): Configuration dictionary containing database
                        connection parameters.
        pool (asyncpg.Pool): Connection pool object.
        pool_min_size (int): Minimum size of the connection pool.
        pool_max_size (int): Maximum size of the connection pool.

    Methods:
        connect(retries=3, delay=2): Establish a connection to PostgreSQL.
        disconnect(): Close the connection pool.
        execute_query(query, *params): Execute a query on PostgreSQL.
    """

    def __init__(self,
                 config: Dict[str, Any],
                 pool_min_size=1,
                 pool_max_size=10):
        self.config = config
        self.config["dsn"] = (
            f"postgresql://{self.config['user']}:{self.config['password']}"
            f"@{self.config['host']}:{self.config['port']}"
            f"/{self.config['database']}"
        )
        self.pool = None
        self.pool_min_size = pool_min_size
        self.pool_max_size = pool_max_size

    async def connect(self, retries=3, delay=2) -> asyncpg.Pool:
        """
        Establish a connection to the PostgreSQL database.

        :param retries: Number of retry attempts.
        :param delay: Delay between retry attempts in seconds.
        :return: Connection pool object.
        """
        for attempt in range(retries):
            try:
                self.pool = await asyncpg.create_pool(
                    dsn=self.config["dsn"],
                    min_size=self.pool_min_size,
                    max_size=self.pool_max_size,
                )
                logger.info("Postgres connection pool created")
                return self.pool
            except asyncpg.PostgresError as e:
                logger.error(
                    "Postgres connection attempt %s failed: %s",
                    attempt + 1, e)
                if attempt < retries - 1:
                    logger.info(
                        "Retrying connection in %s seconds...", delay)

                    # Exponential backoff
                    # Increase the delay for the next attempt
                    await asyncio.sleep(delay)
                    delay *= 2
                else:
                    logger.error("All connection attempts failed")
                    logger.error("Error details: %s", e)
                    raise e

    async def disconnect(self) -> None:
        """
        Close the connection pool.
        """
        if self.pool:
            await self.pool.close()
            logger.info("Postgres connection pool closed")

    async def execute_query(self, query: str, *params: Any) -> List[Any]:
        """
        Execute a query on the PostgreSQL database.

        :param query: SQL query string.
        :param params: Parameters for the query.
        :return: Result of the query execution.
        """
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *params)


class MySQLDBConnection(BaseDBConnection):
    """
    MySQL database connection class.
    This class manages the connection pool and provides methods to connect,
    disconnect, and execute queries.

    Attributes:
        config (dict): Configuration dictionary containing database
        connection parameters.
        pool (aiomysql.Pool): Connection pool object.
        pool_min_size (int): Minimum size of the connection pool.
        pool_max_size (int): Maximum size of the connection pool.

    Methods:
        connect(retries=3, delay=2): Establish a connection to MySQL.
        disconnect(): Close the connection pool.
        execute_query(query, *params): Execute a query on MySQL.
    """

    def __init__(self,
                 config: Dict[str, Any],
                 pool_min_size=1,
                 pool_max_size=10):
        self.config = config
        self.pool = None
        self.pool_min_size = pool_min_size
        self.pool_max_size = pool_max_size

    async def connect(self, retries=3, delay=2) -> aiomysql.Pool:
        """
        Establish a connection to the MySQL database.

        :param retries: Number of retry attempts.
        :param delay: Delay between retry attempts in seconds.
        :return: Connection pool object.
        """
        for attempt in range(retries):
            try:
                self.pool = await aiomysql.create_pool(
                    user=self.config["user"],
                    password=self.config["password"],
                    db=self.config["database"],
                    host=self.config["host"],
                    port=int(self.config["port"]),
                    minsize=self.pool_min_size,
                    maxsize=self.pool_max_size,
                )
                logger.info("MySQL connection pool created")
                return self.pool
            except aiomysql.MySQLError as e:
                logger.error(
                    "MySQL connection attempt %s failed: %s",
                    attempt + 1, e)
                if attempt < retries - 1:
                    logger.info(
                        "Retrying connection in %s seconds...", delay)

                    # Exponential backoff
                    # Increase the delay for the next attempt
                    await asyncio.sleep(delay)
                    delay *= 2
                else:
                    logger.error("All connection attempts failed")
                    logger.error("Error details: %s", e)
                    raise e

    async def disconnect(self):
        """
        Close the connection pool.
        """
        if self.pool:
            await self.pool.wait_closed()
            logger.info("MySQL connection pool closed")

    async def execute_query(self, query: str, *params: Any) -> List[tuple]:
        """
        Execute a query on the MySQL database.

        :param query: SQL query string.
        :param params: Parameters for the query.
        :return: Result of the query execution.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                result = await cursor.fetchall()
                return result


def get_db_connection(config: Dict[str, Any]) -> BaseDBConnection:
    """
    Factory function to get a DB connection instance based on the engine type.

    :param config(DBConfig): Database configuration dictionary.
    :return(BaseDBConnection): Instance of the database connection class.
    :raises ValueError: If the engine type is not supported.
    """
    engine = config.get("engine", "postgres").lower()

    if engine == "postgres":
        return PostgresDBConnection(config)

    if engine == "mysql":
        return MySQLDBConnection(config)

    raise ValueError(f"Unsupported DB engine: {engine}")
