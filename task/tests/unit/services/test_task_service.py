from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from task.src.api.v1.services.task import TaskService
from task.tests.fixtures.db_mocks.mock_uow import get_mock_uow


@pytest.mark.asyncio
async def test_create_task():
    uow = get_mock_uow()

    created_task = MagicMock(
        id=uuid4(),
        title="Created Task",
        description="desc",
        status="todo",
        author_id=uuid4(),
        assignee_id=None,
    )

    uow.task.add_one_and_get_obj.return_value = created_task

    service = TaskService(uow=uow)

    result = await service.create_task({
        "title": "Created Task",
        "description": "desc",
        "status": "todo",
        "author_id": uuid4(),
        "assignee_id": None,
    })

    assert result.title == "Created Task"
    assert result.status == "todo"


@pytest.mark.asyncio
async def test_get_task_not_found():
    uow = get_mock_uow()

    uow.task.get_by_filter_one_or_none.return_value = None

    service = TaskService(uow=uow)

    with pytest.raises(Exception):
        await service.get_task(uuid4())
