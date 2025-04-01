import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
DATABASE_CONFIG = {
    "engine": os.getenv("DB_ENGINE", "postgres"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# AWS S3 configuration
S3_CONFIG = {
    "bucket_name": os.getenv("S3_BUCKET"),
    "region": os.getenv("S3_REGION"),
    "access_key_id": os.getenv("S3_ACCESS_KEY_ID"),
    "secret_access_key": os.getenv("S3_SECRET_ACCESS_KEY"),
}

# Other configurations
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "100"))
FEED_TYPE = os.getenv("FEED_TYPE", "facility")
FEED_NAME = os.getenv("FEED_NAME", "reservewithgoogle.entity")

FEED_FILE_FORMAT = "facility_feed_{timestamp}.json.gz"
METADATA_FILE_FORMAT = "metadata.json"
