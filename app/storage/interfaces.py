from abc import ABC, abstractmethod


class StorageInterface(ABC):
    """
    Interface for storage adapters.
    This interface defines the methods required for uploading files
    to a storage service.
    """

    @abstractmethod
    async def upload_file(self,
                          file_path: str,
                          content_type: str,
                          content_encoding: str,
                          retries: int = 3,
                          initial_delay: float = 2.0) -> bool:
        """
        Upload a file to the storage service.

        :param file_path: Path to the file to be uploaded.
        :param content_type: MIME type of the file.
        :param content_encoding: Content encoding of the file.
        :param retries: Number of retry attempts.
        :param initial_delay: Initial delay between retries (in seconds).
        :raises Exception: If the upload fails after the specified number of retries.
        :return: True if the upload is successful, False otherwise.
        """
