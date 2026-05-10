from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.broker.task_stats_rpc import TaskStatsRpcConsumer


@pytest.mark.asyncio
async def test_task_stats_rpc_handles_user_id_payload():
    service = AsyncMock()
    user_id = uuid4()
    service.get_user_task_stats.return_value = {
        "assigned_tasks_count": 1,
        "watched_tasks_count": 2,
    }
    consumer = TaskStatsRpcConsumer(service=service)

    result = await consumer.handle_payload({"user_id": str(user_id)})

    assert result == {
        "assigned_tasks_count": 1,
        "watched_tasks_count": 2,
    }
    service.get_user_task_stats.assert_awaited_once_with(user_id)
