from fastapi import APIRouter, Depends

from src.api.v1.services.task_watcher import TaskWatcherService
from src.schemas.task_watcher import TaskWatcherRequest, TaskWatcherResponse
from src.utils.constans import WATCHER_ADDED_MSG, WATCHER_REMOVED_MSG

router = APIRouter(prefix="/task-watchers", tags=["task-watchers"])


@router.post("/")
async def add(data: TaskWatcherRequest, service: TaskWatcherService = Depends()):
    await service.add_watcher(data.task_id, data.user_id)
    return TaskWatcherResponse(message=WATCHER_ADDED_MSG)


@router.delete("/")
async def remove(data: TaskWatcherRequest, service: TaskWatcherService = Depends()):
    await service.remove_watcher(data.task_id, data.user_id)
    return TaskWatcherResponse(message=WATCHER_REMOVED_MSG)
