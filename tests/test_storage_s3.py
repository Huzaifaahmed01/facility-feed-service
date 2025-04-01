from unittest.mock import AsyncMock

import pytest

from app.storage.s3 import S3StorageAdapter


@pytest.mark.asyncio
async def test_upload_file(tmp_path):
    s3_mock = AsyncMock()
    s3_mock.put_object.return_value = {}

    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")

    adapter = S3StorageAdapter()
    adapter.upload_file = s3_mock.put_object
    await adapter.upload_file(str(file_path), "text/plain", "utf-8")

    s3_mock.put_object.assert_called_once()
