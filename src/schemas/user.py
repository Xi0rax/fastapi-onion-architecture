from dataclasses import dataclass

from fastapi import Query
from pydantic import UUID4, BaseModel, Field

from src.schemas.filter import TypeFilter
from src.schemas.response import BaseCreateResponse, BaseResponse


class UserID(BaseModel):
    id: UUID4


class CreateUserRequest(BaseModel):
    full_name: str = Field(max_length=100)
    email: str = Field(max_length=120)


class UpdateUserRequest(BaseModel):
    full_name: str | None = None
    email: str | None = None


class UserDB(UserID, CreateUserRequest):
    id: UUID4
    full_name: str
    email: str

    class Config:
        from_attributes = True


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB


class UserResponse(BaseResponse):
    payload: UserDB


class UsersListResponse(BaseResponse):
    payload: list[UserDB]


@dataclass
class UserFilters(TypeFilter):
    ids: list[UUID4] | None = Query(None)
    full_name: list[str] | None = Query(None)
    email: list[str] | None = Query(None)
