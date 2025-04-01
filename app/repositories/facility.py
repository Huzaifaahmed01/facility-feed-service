from typing import List

from app.db.queries import GET_FACILITIES_QUERY
from app.db.connection import BaseDBConnection


class FacilityRepository:
    """
    Repository class for managing facility data.
    This class is responsible for fetching facility data from the database.
    It uses an asynchronous database connection to execute queries.

    Attributes:
        db_connection (BaseDBConnection): DB conn object.

    Methods:
        fetch_facilities_chunk(offset, chunk_size): Fetch a chunk of facility
            data from the database.
    """

    def __init__(self, db_connection: BaseDBConnection):
        self.db_connection = db_connection

    async def fetch_facilities_chunk(self,
                                     offset: int,
                                     chunk_size: int) -> List[dict]:
        """
        Fetch a chunk of facility data from the database.
        This method executes a SQL query to retrieve facility records
        with pagination using OFFSET and LIMIT.

        :param offset: The starting point for the query.
        :param chunk_size: The number of records to fetch.
        :return: A list of facility records.
        """
        return await self.db_connection.execute_query(
            GET_FACILITIES_QUERY,
            offset,
            chunk_size)
