from pydantic import BaseModel, UUID4

from task.src.schemas.response import BaseResponse


class TaskWatcherRequest(BaseModel):
    task_id: UUID4
    user_id: UUID4


class TaskWatcherResponse(BaseResponse):
    message: str
