from fastapi import APIRouter, Depends

from src.api.v1.services.task_executor import TaskExecutorService
from src.schemas.task_executor import TaskExecutorRequest, TaskExecutorResponse
from src.utils.constans import EXECUTOR_ADDED_MSG, EXECUTOR_REMOVED_MSG

router = APIRouter(prefix="/task-executors", tags=["task-executors"])


@router.post("/")
async def add(data: TaskExecutorRequest, service: TaskExecutorService = Depends()):
    await service.add_executor(data.task_id, data.user_id)
    return TaskExecutorResponse(message=EXECUTOR_ADDED_MSG)


@router.delete("/")
async def remove(data: TaskExecutorRequest, service: TaskExecutorService = Depends()):
    await service.remove_executor(data.task_id, data.user_id)
    return TaskExecutorResponse(message=EXECUTOR_REMOVED_MSG)
