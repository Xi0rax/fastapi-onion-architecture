import pytest
from uuid import uuid4

from src.repositories.task import TaskRepository


pytestmark = pytest.mark.db


@pytest.mark.asyncio
async def test_task_repository_add(async_session):
    repo = TaskRepository(async_session)

    task = await repo.add_one_and_get_obj(
        title="Repo Task",
        description="Repo Desc",
        status="todo",
        author_id=uuid4(),
        assignee_id=None,
    )

    assert task.id is not None
    assert task.title == "Repo Task"
