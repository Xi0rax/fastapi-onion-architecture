from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.api.v1.services.column import ColumnService
from src.schemas.column import (
    CreateColumnRequest,
    UpdateColumnRequest,
    CreateColumnResponse,
    ColumnResponse,
    ColumnsListResponse,
    ColumnDB
)

router = APIRouter(prefix="/columns", tags=["columns"])


@router.post("/")
async def create(data: CreateColumnRequest, service: ColumnService = Depends()) -> CreateColumnResponse:
    obj = await service.create_column(data.model_dump())
    return CreateColumnResponse(payload=ColumnDB.model_validate(obj))


@router.get("/{obj_id}")
async def get(obj_id: UUID4, service: ColumnService = Depends()) -> ColumnResponse:
    obj = await service.get_column(obj_id)
    return ColumnResponse(payload=ColumnDB.model_validate(obj))


@router.get("/")
async def list(service: ColumnService = Depends()) -> ColumnsListResponse:
    objs = await service.get_columns()
    return ColumnsListResponse(
        payload=[ColumnDB.model_validate(obj) for obj in objs]
    )


@router.patch("/{obj_id}")
async def update(
        obj_id: UUID4,
        data: UpdateColumnRequest,
        service: ColumnService = Depends(),
) -> ColumnResponse:
    obj = await service.update_column(obj_id, data.model_dump(exclude_unset=True))
    return ColumnResponse(payload=ColumnDB.model_validate(obj))


@router.delete("/{obj_id}")
async def delete(obj_id: UUID4, service: ColumnService = Depends()) -> None:
    await service.delete_column(obj_id)
