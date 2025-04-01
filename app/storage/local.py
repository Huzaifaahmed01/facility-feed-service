import os

from app.storage.interfaces import StorageInterface

from app.utils.logger import get_logger

logger = get_logger(__name__)


class LocalStorageAdapter(StorageInterface):
    async def upload_file(self,
                          file_path: str,
                          content_type: str,
                          content_encoding: str,
                          retries: int = 3,
                          initial_delay: float = 2.0) -> bool:
        destination_dir = "local_storage"

        os.makedirs(destination_dir, exist_ok=True)
        destination_path = os.path.join(
            destination_dir, os.path.basename(file_path))

        try:
            with open(file_path, 'rb') as source_file:
                with open(destination_path, 'wb') as dest_file:
                    dest_file.write(source_file.read())
            logger.info("File %s uploaded successfully to %s.",
                        file_path, destination_path)

            try:
                os.remove(file_path)
                logger.info(
                    "File %s deleted after successful upload.", file_path)
            except OSError as delete_err:
                logger.error("Failed to delete file %s: %s",
                             file_path, delete_err)

            return True
        except OSError as e:
            logger.error("Failed to upload file %s: %s", file_path, e)
            return False
