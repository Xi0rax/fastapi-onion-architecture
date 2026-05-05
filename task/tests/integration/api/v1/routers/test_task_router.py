import pytest

from task.tests.fixtures.testing_cases.task_cases import VALID_TASK_PAYLOAD


@pytest.mark.asyncio
async def test_post_task(client):
    response = await client.post("/tasks/", json=VALID_TASK_PAYLOAD)

    assert response.status_code == 201

    data = response.json()

    assert data["error"] is False
    assert data["payload"]["title"] == VALID_TASK_PAYLOAD["title"]


@pytest.mark.asyncio
async def test_get_tasks(client):
    response = await client.get("/tasks/")

    assert response.status_code == 200
    assert "payload" in response.json()


@pytest.mark.asyncio
async def test_get_tasks_filtered(client):
    response = await client.get("/tasks/?status=todo")

    assert response.status_code == 200
    assert "payload" in response.json()
