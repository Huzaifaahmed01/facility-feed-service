import json
import time
from abc import ABC, abstractmethod
from typing import List, Dict

from config import METADATA_FILE_FORMAT

from app.utils.logger import get_logger

logger = get_logger(__name__)


class FeedGeneratorInterface(ABC):
    """
    Interface for generating feed files from database records.
    This interface defines the methods required to generate feed files
    and transform records into the desired format.
    """

    @abstractmethod
    def generate_feed_file(self, records: List[Dict], timestamp: int = None) -> str:
        """
        Generate a feed file given a set of records and a timestamp.

        :param records: List of records to be included in the feed.
        :return: Path to the generated feed file.
        """

    @abstractmethod
    def transform_record(self, record: Dict) -> Dict:
        """
        Transform a database record into the feed-specific format.

        :param record: Dictionary containing the record data.
        :return: Transformed record as a dictionary.
        """

    @staticmethod
    def generate_metadata_file(
            feed_files: List[str],
            feed_name: str,
            timestamp: int = None) -> str:
        """
        Generate a metadata descriptor file listing all feed files.

        :param feed_files: List of feed files generated.
        :param feed_name: Name of the feed.
        :return: Path to the generated metadata file.
        """

        metadata = {
            "generation_timestamp": timestamp or int(time.time()),
            "name": feed_name,
            "data_file": feed_files
        }

        metadata_filename = METADATA_FILE_FORMAT

        try:
            with open(metadata_filename, "w", encoding="utf-8") as f:
                json.dump(metadata, f)

            logger.info("Metadata file generated: %s", metadata_filename)

            return metadata_filename
        except (IOError, OSError) as e:
            logger.error("Error generating metadata file: %s", e)

            return None
