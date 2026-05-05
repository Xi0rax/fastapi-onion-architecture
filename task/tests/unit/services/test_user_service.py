from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from task.src.api.v1.services.user import UserService
from task.tests.fixtures.db_mocks.mock_uow import get_mock_uow


@pytest.mark.asyncio
async def test_get_user():
    uow = get_mock_uow()

    mock_user = MagicMock(
        id=uuid4(),
        full_name="John Doe",
        email="john@test.com",
    )

    uow.user.get_by_filter_one_or_none.return_value = mock_user

    service = UserService(uow=uow)

    result = await service.get_user(uuid4())

    assert result.email == "john@test.com"
