from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, UUID4, Field, field_validator

from task_service.src.models.enums import task_status_enum
from task_service.src.schemas.filter import TypeFilter
from task_service.src.schemas.response import BaseCreateResponse, BaseResponse
from task_service.src.utils.constans import TITLE_TOO_SHORT_MSG, INVALID_STATUS_MSG

ALLOWED_STATUSES = set(task_status_enum.enums)


class TaskID(BaseModel):
    id: UUID4


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str | None = None
    status: str
    author_id: UUID4
    assignee_id: UUID4 | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError(TITLE_TOO_SHORT_MSG)
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ALLOWED_STATUSES:
            raise ValueError(INVALID_STATUS_MSG)
        return v


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=3)
    description: str | None = None
    status: str | None = None
    assignee_id: UUID4 | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        if v is not None and v not in ALLOWED_STATUSES:
            raise ValueError(INVALID_STATUS_MSG)
        return v


class TaskDB(TaskID, TaskCreateRequest):
    id: UUID4
    title: str
    description: str | None
    status: str
    author_id: UUID4
    assignee_id: UUID4 | None

    class Config:
        from_attributes = True


class CreateTaskResponse(BaseCreateResponse):
    payload: TaskDB


class TaskResponse(BaseResponse):
    payload: TaskDB


class TasksListResponse(BaseResponse):
    payload: list[TaskDB]


@dataclass
class TaskFilters(TypeFilter):
    ids: list[UUID4] | None = Query(None)
    author_id: list[UUID4] | None = Query(None)
    assignee_id: list[UUID4] | None = Query(None)
    status: list[str] | None = Query(None)
