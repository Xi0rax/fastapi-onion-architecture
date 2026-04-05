from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.api.v1.services.user import UserService
from src.schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRequest,
    UserFilters,
    UserResponse,
    UsersListResponse,
    UserDB
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=HTTP_201_CREATED)
async def create_user(
        user: CreateUserRequest,
        service: UserService = Depends(),
) -> CreateUserResponse:
    created_user = await service.create_user(user.model_dump())
    return CreateUserResponse(payload=UserDB.model_validate(created_user))


@router.get("/{user_id}", status_code=HTTP_200_OK)
async def get_user(
        user_id: UUID4,
        service: UserService = Depends(),
) -> UserResponse:
    user = await service.get_user(user_id)
    return UserResponse(payload=UserDB.model_validate(user))


@router.put("/{user_id}", status_code=HTTP_200_OK)
async def update_user(
        user_id: UUID4,
        user: UpdateUserRequest,
        service: UserService = Depends(),
) -> UserResponse:
    updated_user = await service.update_user(
        user_id,
        user.model_dump(exclude_unset=True),
    )
    return UserResponse(payload=UserDB.model_validate(updated_user))


@router.delete("/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: UUID4,
        service: UserService = Depends(),
) -> None:
    await service.delete_user(user_id)


@router.get("/", status_code=HTTP_200_OK)
async def get_users(
        filters: UserFilters = Depends(),
        service: UserService = Depends(),
) -> UsersListResponse:
    users = await service.get_users(filters)
    return UsersListResponse(
        payload=[UserDB.model_validate(user) for user in users]
    )
