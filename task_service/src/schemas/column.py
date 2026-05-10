from pydantic import BaseModel, UUID4, Field

from task_service.src.schemas.response import BaseCreateResponse, BaseResponse


class ColumnID(BaseModel):
    id: UUID4


class CreateColumnRequest(BaseModel):
    name: str = Field(max_length=100)
    board_id: UUID4


class UpdateColumnRequest(BaseModel):
    name: str | None = None


class ColumnDB(ColumnID, CreateColumnRequest):
    id: UUID4
    name: str
    board_id: UUID4

    class Config:
        from_attributes = True


class CreateColumnResponse(BaseCreateResponse):
    payload: ColumnDB


class ColumnResponse(BaseResponse):
    payload: ColumnDB


class ColumnsListResponse(BaseResponse):
    payload: list[ColumnDB]
