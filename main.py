import asyncio

from config import DATABASE_CONFIG, CHUNK_SIZE, FEED_NAME

from app.db.connection import get_db_connection
from app.repositories.facility import FacilityRepository

from app.feed.factory import FeedGeneratorFactory
from app.feed.interfaces import FeedGeneratorInterface

from app.storage.interfaces import StorageInterface
from app.storage.s3 import S3StorageAdapter
# from app.storage.localstorage import LocalStorageAdapter

from app.utils.logger import get_logger

logger = get_logger(__name__)


class FacilityFeedService:
    """
    Service class for processing and uploading facility feed data.
    This class is responsible for fetching facility data from the database,
    generating feed files, and uploading them to an S3 bucket.
    It uses a repository pattern to interact with the database and a
    storage adapter to handle file uploads.

    Attributes:
        repository (FacilityRepository): Repository instance for fetching
            facility data.
        storage_adapter (StorageInterface): Storage adapter instance for
            uploading files to S3.
        feed_generator (FeedGeneratorInterface): Feed generator instance for
            creating feed files.

    Methods:
        run(): Main method to execute the feed processing and upload
            process.
    """

    def __init__(self,
                 repository: FacilityRepository,
                 storage_adapter: StorageInterface,
                 feed_generator: FeedGeneratorInterface):
        self.repository = repository
        self.storage_adapter = storage_adapter
        self.feed_generator = feed_generator
        self.chunk_size = CHUNK_SIZE

    async def run(self):
        feed_files = []
        offset = 0

        while True:
            records = await self.repository.fetch_facilities_chunk(
                offset,
                self.chunk_size)
            logger.info("Fetched %d records from the database.", len(records))

            if not records:
                logger.info("No more records to process.")
                break

            feed_file = self.feed_generator.generate_feed_file(records)

            if not feed_file:
                logger.error(
                    "Failed to generate feed file for offset %d.", offset)
                break

            feed_files.append(feed_file)
            logger.info("Generated feed file: %s", feed_file)

            await self.storage_adapter.upload_file(
                feed_file,
                "application/json",
                "gzip")
            logger.info("Uploaded %s to storage.", feed_file)

            offset += self.chunk_size

        metadata_file = self.feed_generator.generate_metadata_file(
            feed_files,
            FEED_NAME)
        await self.storage_adapter.upload_file(
            metadata_file,
            "application/json",
            "identity")
        logger.info("Uploaded metadata file: %s to storage.", metadata_file)
        logger.info("Feed processing and upload completed.")


if __name__ == "__main__":
    async def main():
        # Initialize database connection and repository
        db_conn_instance = get_db_connection(DATABASE_CONFIG)
        await db_conn_instance.connect()
        repository = FacilityRepository(db_conn_instance)

        # Initialize feed generator and storage adapter
        feed_generator = FeedGeneratorFactory.get_feed_generator()
        storage_adapter = S3StorageAdapter()

        # Initialize and run the service
        service = FacilityFeedService(
            repository,
            storage_adapter,
            feed_generator)

        await service.run()

    asyncio.run(main())
