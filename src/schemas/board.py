from pydantic import BaseModel, UUID4, Field

from src.schemas.response import BaseCreateResponse, BaseResponse


class BoardID(BaseModel):
    id: UUID4


class CreateBoardRequest(BaseModel):
    name: str = Field(max_length=100)


class UpdateBoardRequest(BaseModel):
    name: str | None = None


class BoardDB(BoardID, CreateBoardRequest):
    id: UUID4
    name: str

    class Config:
        from_attributes = True


class CreateBoardResponse(BaseCreateResponse):
    payload: BoardDB


class BoardResponse(BaseResponse):
    payload: BoardDB


class BoardsListResponse(BaseResponse):
    payload: list[BoardDB]
