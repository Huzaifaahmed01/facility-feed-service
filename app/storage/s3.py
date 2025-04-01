import os

import asyncio
import aioboto3
from botocore.exceptions import BotoCoreError, ClientError

from config import S3_CONFIG
from app.storage.interfaces import StorageInterface

from app.utils.logger import get_logger

logger = get_logger(__name__)


class S3StorageAdapter(StorageInterface):
    def __init__(self):
        self.session = aioboto3.Session(
            aws_access_key_id=S3_CONFIG["access_key_id"],
            aws_secret_access_key=S3_CONFIG["secret_access_key"],
            region_name=S3_CONFIG["region"]
        )

    async def upload_file(self,
                          file_path: str,
                          content_type: str,
                          content_encoding: str,
                          retries: int = 3,
                          initial_delay: float = 2.0) -> bool:
        """
        Upload a file to S3 with retry logic in case of errors.

        :param file_path: Path to the file to upload.
        :param content_type: MIME type of the file.
        :param content_encoding: Content encoding of the file.
        :param retries: Number of retry attempts.
        :param initial_delay: Initial delay between retries (in seconds).
        """
        for attempt in range(1, retries + 1):
            try:
                async with self.session.client('s3') as s3_client:
                    with open(file_path, 'rb') as file_data:
                        await s3_client.upload_fileobj(
                            file_data,
                            S3_CONFIG["bucket_name"],
                            file_path,
                            ExtraArgs={
                                'ContentType': content_type,
                                'ContentEncoding': content_encoding
                            }
                        )
                logger.info(
                    "File %s uploaded successfully on attempt %s.",
                    file_path,
                    attempt)

                # Delete the file after successful upload
                try:
                    os.remove(file_path)
                    logger.info(
                        "File %s deleted after successful upload.", file_path)
                except OSError as delete_err:
                    logger.error("Failed to delete file %s: %s",
                                 file_path, delete_err)

                return True
            except (BotoCoreError, ClientError) as e:
                logger.error(
                    "Attempt %s to upload file %s failed: %s",
                    attempt,
                    file_path,
                    e)
                if attempt < retries:
                    delay = initial_delay * (2 ** (attempt - 1))
                    logger.info("Retrying in %s seconds...", delay)
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        "All %s attempts to upload file %s have failed.",
                        retries,
                        file_path
                    )
                    return False
        return False
