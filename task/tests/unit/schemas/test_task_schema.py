import pytest
from pydantic import ValidationError

from task.src.schemas.task import TaskCreateRequest
from task.tests.utils import fake_uuid


def test_task_title_validation():
    with pytest.raises(ValidationError):
        TaskCreateRequest(
            title="ab",
            description="desc",
            status="todo",
            author_id=fake_uuid(),
            assignee_id=None,
        )


def test_task_status_validation():
    with pytest.raises(ValidationError):
        TaskCreateRequest(
            title="Valid title",
            description="desc",
            status="invalid_status",
            author_id=fake_uuid(),
            assignee_id=None,
        )
