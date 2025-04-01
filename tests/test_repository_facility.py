from unittest.mock import AsyncMock

import pytest

from app.repositories.facility import FacilityRepository


@pytest.mark.asyncio
async def test_fetch_facilities_chunk():
    mock_db = AsyncMock()
    mock_db.execute_query.return_value = [{"id": 1, "name": "Test Facility"}]

    repo = FacilityRepository(mock_db)
    result = await repo.fetch_facilities_chunk(0, 10)

    assert result == [{"id": 1, "name": "Test Facility"}]
    mock_db.execute_query.assert_called_once()
