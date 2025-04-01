from config import FEED_TYPE

from app.feed.facilityfeed_generator import FacilityFeedGenerator
from app.feed.interfaces import FeedGeneratorInterface


class FeedGeneratorFactory:
    """Factory class to create feed generator instances."""

    @staticmethod
    def get_feed_generator(feed_type=None) -> FeedGeneratorInterface:
        """
        Get the appropriate feed generator based on the configuration.

        :return: Instance of the feed generator.
        """
        feed_type = feed_type or FEED_TYPE

        if feed_type == "facility":
            return FacilityFeedGenerator()

        raise ValueError(f"Unsupported feed type: {feed_type}")
