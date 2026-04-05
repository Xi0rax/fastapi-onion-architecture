from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.api.v1.services.task import TaskService
from src.schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskFilters,
    CreateTaskResponse,
    TaskResponse,
    TasksListResponse,
    TaskDB
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=HTTP_201_CREATED)
async def create_task(
        task: TaskCreateRequest,
        service: TaskService = Depends(),
) -> CreateTaskResponse:
    created = await service.create_task(task.model_dump())
    return CreateTaskResponse(payload=TaskDB.model_validate(created))


@router.get("/{task_id}", status_code=HTTP_200_OK)
async def get_task(
        task_id: UUID4,
        service: TaskService = Depends(),
) -> TaskResponse:
    task = await service.get_task(task_id)
    return TaskResponse(payload=TaskDB.model_validate(task))


@router.get("/", status_code=HTTP_200_OK)
async def get_tasks(
        filters: TaskFilters = Depends(),
        service: TaskService = Depends(),
) -> TasksListResponse:
    tasks = await service.get_tasks(filters)
    return TasksListResponse(
        payload=[TaskDB.model_validate(task) for task in tasks]
    )


@router.patch("/{task_id}", status_code=HTTP_200_OK)
async def update_task(
        task_id: UUID4,
        task: TaskUpdateRequest,
        service: TaskService = Depends(),
) -> TaskResponse:
    updated = await service.update_task(
        task_id,
        task.model_dump(exclude_unset=True),
    )
    return TaskResponse(payload=TaskDB.model_validate(updated))


@router.delete("/{task_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: UUID4,
        service: TaskService = Depends(),
) -> None:
    await service.delete_task(task_id)
