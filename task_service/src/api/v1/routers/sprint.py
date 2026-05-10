from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.api.v1.services.sprint import SprintService
from src.schemas.sprint import (
    CreateSprintRequest,
    UpdateSprintRequest,
    CreateSprintResponse,
    SprintResponse,
    SprintsListResponse,
    SprintDB
)

router = APIRouter(prefix="/sprints", tags=["sprints"])


@router.post("/")
async def create(data: CreateSprintRequest, service: SprintService = Depends()) -> CreateSprintResponse:
    obj = await service.create_sprint(data.model_dump())
    return CreateSprintResponse(payload=SprintDB.model_validate(obj))


@router.get("/{obj_id}")
async def get(obj_id: UUID4, service: SprintService = Depends()) -> SprintResponse:
    obj = await service.get_sprint(obj_id)
    return SprintResponse(payload=SprintDB.model_validate(obj))


@router.get("/")
async def list(service: SprintService = Depends()) -> SprintsListResponse:
    objs = await service.get_sprints()
    return SprintsListResponse(
        payload=[SprintDB.model_validate(obj) for obj in objs]
    )


@router.patch("/{obj_id}")
async def update(
        obj_id: UUID4,
        data: UpdateSprintRequest,
        service: SprintService = Depends(),
) -> SprintResponse:
    obj = await service.update_sprint(obj_id, data.model_dump(exclude_unset=True))
    return SprintResponse(payload=SprintDB.model_validate(obj))


@router.delete("/{obj_id}")
async def delete(obj_id: UUID4, service: SprintService = Depends()) -> None:
    await service.delete_sprint(obj_id)
