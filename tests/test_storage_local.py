import os
from unittest.mock import patch, mock_open

import pytest
import pytest_asyncio

from app.storage.local import LocalStorageAdapter


@pytest_asyncio.fixture
def storage_adapter():
    return LocalStorageAdapter()


@pytest.mark.asyncio
@patch("builtins.open", new_callable=mock_open, read_data=b"file content")
@patch("os.makedirs")
@patch("os.remove")
async def test_upload_file(mock_remove,
                           mock_makedirs,
                           mock_file_open,
                           storage_adapter):  # pylint: disable=redefined-outer-name
    file_path = "test_file.txt"
    destination_path = os.path.join("local_storage", "test_file.txt")

    result = await storage_adapter.upload_file(
        file_path,
        "text/plain",
        "utf-8")

    assert result is True
    mock_makedirs.assert_called_once_with("local_storage", exist_ok=True)
    # Ensure source file was opened
    mock_file_open.assert_any_call(file_path, 'rb')
    # Ensure destination file was opened
    mock_file_open.assert_any_call(destination_path, 'wb')
    # Ensure file deletion after upload
    mock_remove.assert_called_once_with(file_path)


@pytest.mark.asyncio
@patch("builtins.open", side_effect=OSError("Failed to open file"))
@patch("os.makedirs")
async def test_upload_file_failure(mock_makedirs,
                                   mock_file_open,
                                   # pylint: disable=redefined-outer-name
                                   storage_adapter):
    file_path = "test_file.txt"

    result = await storage_adapter.upload_file(
        file_path,
        "text/plain",
        "utf-8")

    assert result is False
    mock_makedirs.assert_called_once_with("local_storage", exist_ok=True)
    # Ensure it attempted to open the file
    mock_file_open.assert_called_once_with(file_path, 'rb')
