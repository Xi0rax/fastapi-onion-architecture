from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from auth_service.src.broker.user_info_rpc import UserInfoRpcConsumer


@pytest.mark.asyncio
async def test_user_info_rpc_returns_profile_payload():
    user_id = uuid4()
    service = AsyncMock()
    service.get_user_profile.return_value = SimpleNamespace(
        id=user_id,
        email="user@example.com",
        full_name="User Example",
    )
    consumer = UserInfoRpcConsumer(service=service)

    result = await consumer.handle_payload({"user_id": str(user_id)})

    assert result == {
        "id": str(user_id),
        "email": "user@example.com",
        "full_name": "User Example",
    }
