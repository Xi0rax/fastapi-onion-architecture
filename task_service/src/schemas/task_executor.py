from pydantic import BaseModel, UUID4

from task_service.src.schemas.response import BaseResponse


class TaskExecutorRequest(BaseModel):
    task_id: UUID4
    user_id: UUID4


class TaskExecutorResponse(BaseResponse):
    message: str
