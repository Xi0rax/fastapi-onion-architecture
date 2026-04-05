from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, field_validator, UUID4

from src.models.enums import task_status_enum
from src.schemas.filter import TypeFilter
from src.utils.constans import TITLE_TOO_SHORT_MSG, INVALID_STATUS_MSG

ALLOWED_STATUSES = set(task_status_enum.enums)


class TaskCreateRequest(BaseModel):
    title: str
    description: str | None
    status: str
    author_id: UUID4
    assignee_id: UUID4 | None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if len(v) < 3:
            raise ValueError(TITLE_TOO_SHORT_MSG)
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ALLOWED_STATUSES:
            raise ValueError(INVALID_STATUS_MSG)
        return v


class TaskUpdateRequest(BaseModel):
    title: str | None
    description: str | None
    status: str | None


class TaskResponse(BaseModel):
    id: UUID4
    title: str
    description: str | None
    status: str
    author_id: UUID4
    assignee_id: UUID4 | None

    class Config:
        from_attributes = True


@dataclass
class TaskFilters(TypeFilter):
    ids: list[UUID4] | None = Query(None)
    author_id: list[UUID4] | None = Query(None)
    assignee_id: list[UUID4] | None = Query(None)
    status: list[str] | None = Query(None)
