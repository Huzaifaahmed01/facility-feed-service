import gzip
import json
import time
from typing import Any, Dict, List

from config import FEED_FILE_FORMAT

from app.feed.interfaces import FeedGeneratorInterface
from app.utils.logger import get_logger


logger = get_logger(__name__)


class FacilityFeedGenerator(FeedGeneratorInterface):
    """Generates facility feed files in JSON format."""

    def transform_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a single record into the desired format.

        :param record: Dictionary containing facility data.
        :return: Transformed record as a dictionary.
        """
        return {
            "entity_id": record['id'],
            "name": record["name"],
            "telephone": record["phone"],
            "url": record["url"],
            "location": {
                "latitude": record["latitude"],
                "longitude": record["longitude"],
                "address": {
                    "country": record["country"],
                    "locality": record["locality"],
                    "region": record["region"],
                    "postal_code": record["postal_code"],
                    "street_address": record["street_address"],
                }
            }
        }

    def generate_feed_file(self,
                           records: List[Dict[str, Any]],
                           timestamp: int = None) -> str:
        """
        Generate a feed file from the provided records.

        :param records: List of facility records.
        :return: Path to the generated feed file.
        """

        feed_data = {"data": [self.transform_record(
            record) for record in records]}

        filename = FEED_FILE_FORMAT.format(
            # milliseconds because of async calls
            timestamp=timestamp or int(time.time()*1000)
        )

        try:
            with gzip.open(filename, 'wt', encoding='utf-8') as f:
                json.dump(feed_data, f)
            logger.info("Feed file %s generated successfully.", filename)
            return filename
        except (OSError, IOError) as e:
            logger.error(
                "Error writing to file %s: %s", filename, str(e))
            return None
