import json
import gzip

from app.feed.facilityfeed_generator import FacilityFeedGenerator


def test_transform_record():
    generator = FacilityFeedGenerator()
    record = {
        "id": 1,
        "name": "Facility A",
        "phone": "1234567890",
        "url": "http://example.com",
        "latitude": 12.34,
        "longitude": 56.78,
        "country": "Country",
        "locality": "Locality",
        "region": "Region",
        "postal_code": "12345",
        "street_address": "123 Street"
    }
    transformed = generator.transform_record(record)

    assert transformed["entity_id"] == 1
    assert transformed["name"] == "Facility A"
    assert transformed["telephone"] == "1234567890"
    assert transformed["url"] == "http://example.com"
    assert transformed["location"]["latitude"] == 12.34
    assert transformed["location"]["longitude"] == 56.78
    assert transformed["location"]["address"]["country"] == "Country"
    assert transformed["location"]["address"]["locality"] == "Locality"
    assert transformed["location"]["address"]["region"] == "Region"
    assert transformed["location"]["address"]["postal_code"] == "12345"
    assert transformed["location"]["address"]["street_address"] == "123 Street"
    assert transformed["location"]["address"]["country"] == "Country"
    assert transformed["location"]["address"]["locality"] == "Locality"


def test_generate_feed_file():
    generator = FacilityFeedGenerator()
    sample_data = [
        {
            "id": 1,
            "name": "Facility A",
            "phone": "1234567890",
            "url": "http://example.com",
            "latitude": 12.34,
            "longitude": 56.78,
            "country": "Country",
            "locality": "Locality",
            "region": "Region",
            "postal_code": "12345",
            "street_address": "123 Street"
        }
    ]

    file_path = generator.generate_feed_file(sample_data, 1234567890)

    assert file_path.endswith(".gz")

    with gzip.open(file_path, 'rt', encoding="utf-8") as f:
        data = json.load(f)
        assert "data" in data
        assert len(data["data"]) == 1
