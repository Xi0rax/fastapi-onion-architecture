from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.api.v1.services.group import GroupService
from src.schemas.group import (
    CreateGroupRequest,
    UpdateGroupRequest,
    CreateGroupResponse,
    GroupResponse,
    GroupsListResponse,
    GroupDB
)

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("/")
async def create(data: CreateGroupRequest, service: GroupService = Depends()) -> CreateGroupResponse:
    obj = await service.create_group(data.model_dump())
    return CreateGroupResponse(payload=GroupDB.model_validate(obj))


@router.get("/{obj_id}")
async def get(obj_id: UUID4, service: GroupService = Depends()) -> GroupResponse:
    obj = await service.get_group(obj_id)
    return GroupResponse(payload=GroupDB.model_validate(obj))


@router.get("/")
async def list(service: GroupService = Depends()) -> GroupsListResponse:
    objs = await service.get_groups()
    return GroupsListResponse(
        payload=[GroupDB.model_validate(obj) for obj in objs]
    )


@router.patch("/{obj_id}")
async def update(
        obj_id: UUID4,
        data: UpdateGroupRequest,
        service: GroupService = Depends(),
) -> GroupResponse:
    obj = await service.update_group(obj_id, data.model_dump(exclude_unset=True))
    return GroupResponse(payload=GroupDB.model_validate(obj))


@router.delete("/{obj_id}")
async def delete(obj_id: UUID4, service: GroupService = Depends()) -> None:
    await service.delete_group(obj_id)
