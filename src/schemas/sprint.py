from datetime import date

from pydantic import BaseModel, UUID4, Field

from src.schemas.response import BaseCreateResponse, BaseResponse


class SprintID(BaseModel):
    id: UUID4


class CreateSprintRequest(BaseModel):
    name: str = Field(max_length=100)
    start_date: date
    end_date: date


class UpdateSprintRequest(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class SprintDB(SprintID, CreateSprintRequest):
    id: UUID4
    name: str
    start_date: date
    end_date: date

    class Config:
        from_attributes = True


class CreateSprintResponse(BaseCreateResponse):
    payload: SprintDB


class SprintResponse(BaseResponse):
    payload: SprintDB


class SprintsListResponse(BaseResponse):
    payload: list[SprintDB]
