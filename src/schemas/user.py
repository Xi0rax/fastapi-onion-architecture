from dataclasses import dataclass
from fastapi import Query
from pydantic import BaseModel, EmailStr, UUID4, Field

from src.schemas.filter import TypeFilter


class CreateUserRequest(BaseModel):
    full_name: str = Field(min_length=3)
    email: EmailStr


class UpdateUserRequest(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: UUID4
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


@dataclass
class UserFilters(TypeFilter):
    ids: list[UUID4] | None = Query(None)
    full_name: list[str] | None = Query(None)
    email: list[str] | None = Query(None)