from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from auth_service.src.api.v1.services.auth import AuthService
from auth_service.src.schemas.auth import LoginRequest, RegisterRequest
from auth_service.src.security.password import hash_password
from auth_service.tests.fixtures.mock_uow import get_mock_uow


@pytest.mark.asyncio
async def test_register_creates_user_and_publishes_notification():
    uow = get_mock_uow()
    producer = AsyncMock()
    task_stats_client = AsyncMock()
    user_id = uuid4()
    created_user = SimpleNamespace(id=user_id, email="new@example.com", full_name="New User")

    uow.user.get_by_filter_one_or_none.return_value = None
    uow.user.add_one_and_get_obj.return_value = created_user

    service = AuthService(uow=uow, producer=producer, task_stats_client=task_stats_client)

    result = await service.register(
        RegisterRequest(email="new@example.com", password="secret-pass", full_name="New User")
    )

    assert result == created_user
    producer.publish.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_rejects_existing_user():
    uow = get_mock_uow()
    uow.user.get_by_filter_one_or_none.return_value = SimpleNamespace(id=uuid4())

    service = AuthService(uow=uow, producer=AsyncMock(), task_stats_client=AsyncMock())

    with pytest.raises(HTTPException) as exc:
        await service.register(RegisterRequest(email="taken@example.com", password="secret-pass", full_name="User"))

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_login_returns_token_for_valid_credentials():
    uow = get_mock_uow()
    user = SimpleNamespace(id=uuid4(), password_hash=hash_password("secret-pass"))
    uow.user.get_by_filter_one_or_none.return_value = user

    service = AuthService(uow=uow, producer=AsyncMock(), task_stats_client=AsyncMock())

    token = await service.login(LoginRequest(email="new@example.com", password="secret-pass"))

    assert token


@pytest.mark.asyncio
async def test_login_rejects_invalid_credentials():
    uow = get_mock_uow()
    uow.user.get_by_filter_one_or_none.return_value = None

    service = AuthService(uow=uow, producer=AsyncMock(), task_stats_client=AsyncMock())

    with pytest.raises(HTTPException) as exc:
        await service.login(LoginRequest(email="new@example.com", password="wrong-pass"))

    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_user_info_merges_profile_and_task_stats():
    uow = get_mock_uow()
    user_id = uuid4()
    user = SimpleNamespace(id=user_id, email="new@example.com", full_name="New User")
    task_stats_client = AsyncMock()
    task_stats_client.get_user_task_stats.return_value = {
        "assigned_tasks_count": 4,
        "watched_tasks_count": 5,
    }
    uow.user.get_by_filter_one_or_none.return_value = user

    service = AuthService(uow=uow, producer=AsyncMock(), task_stats_client=task_stats_client)

    result = await service.get_user_info(user_id)

    assert result == {
        "id": user_id,
        "email": "new@example.com",
        "full_name": "New User",
        "assigned_tasks_count": 4,
        "watched_tasks_count": 5,
    }
