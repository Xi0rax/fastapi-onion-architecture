from types import SimpleNamespace
from uuid import uuid4

import pytest

from src.api.v1.services.task import TaskService
from src.main import app
from tests.constants import BASE_ENDPOINT_URL
from tests.fixtures.testing_cases.task_cases import VALID_TASK_PAYLOAD
from tests.utils import prepare_payload


@pytest.fixture
def task_service_override():
    task = SimpleNamespace(
        id=uuid4(),
        title=VALID_TASK_PAYLOAD["title"],
        description=VALID_TASK_PAYLOAD["description"],
        status=VALID_TASK_PAYLOAD["status"],
        author_id=VALID_TASK_PAYLOAD["author_id"],
        assignee_id=VALID_TASK_PAYLOAD["assignee_id"],
    )

    class FakeTaskService:
        async def create_task(self, data):
            return SimpleNamespace(id=uuid4(), **data)

        async def get_tasks(self, filters):
            return [task]

    app.dependency_overrides[TaskService] = FakeTaskService
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_post_task(client, task_service_override):
    response = await client.post(f"{BASE_ENDPOINT_URL}/tasks/", json=VALID_TASK_PAYLOAD)

    assert response.status_code == 201

    assert response.json()["error"] is False
    assert prepare_payload(response)["title"] == VALID_TASK_PAYLOAD["title"]


@pytest.mark.asyncio
async def test_get_tasks(client, task_service_override):
    response = await client.get(f"{BASE_ENDPOINT_URL}/tasks/")

    assert response.status_code == 200
    assert "payload" in response.json()


@pytest.mark.asyncio
async def test_get_tasks_filtered(client, task_service_override):
    response = await client.get(f"{BASE_ENDPOINT_URL}/tasks/?status=todo")

    assert response.status_code == 200
    assert "payload" in response.json()
