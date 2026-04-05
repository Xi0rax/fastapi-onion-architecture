from pydantic import BaseModel, UUID4, Field

from src.schemas.response import BaseCreateResponse, BaseResponse


class GroupID(BaseModel):
    id: UUID4


class CreateGroupRequest(BaseModel):
    name: str = Field(max_length=100)


class UpdateGroupRequest(BaseModel):
    name: str | None = None


class GroupDB(GroupID, CreateGroupRequest):
    id: UUID4
    name: str

    class Config:
        from_attributes = True


class CreateGroupResponse(BaseCreateResponse):
    payload: GroupDB


class GroupResponse(BaseResponse):
    payload: GroupDB


class GroupsListResponse(BaseResponse):
    payload: list[GroupDB]
