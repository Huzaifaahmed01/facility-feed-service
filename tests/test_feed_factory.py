import pytest

from app.feed.factory import FeedGeneratorFactory
from app.feed.facilityfeed_generator import FacilityFeedGenerator


def test_get_feed_generator():
    generator = FeedGeneratorFactory.get_feed_generator("facility")
    assert isinstance(generator, FacilityFeedGenerator)


def test_get_feed_generator_invalid():
    with pytest.raises(ValueError):
        FeedGeneratorFactory.get_feed_generator("invalid_feed_type")
