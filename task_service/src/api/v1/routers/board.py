from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.api.v1.services.board import BoardService
from src.schemas.board import (
    CreateBoardRequest,
    UpdateBoardRequest,
    CreateBoardResponse,
    BoardResponse,
    BoardsListResponse,
    BoardDB
)

router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/")
async def create(
        data: CreateBoardRequest,
        service: BoardService = Depends(),
) -> CreateBoardResponse:
    obj = await service.create_board(data.model_dump())
    return CreateBoardResponse(payload=BoardDB.model_validate(obj))


@router.get("/{obj_id}")
async def get(
        obj_id: UUID4,
        service: BoardService = Depends(),
) -> BoardResponse:
    obj = await service.get_board(obj_id)
    return BoardResponse(payload=BoardDB.model_validate(obj))


@router.get("/")
async def list(
        service: BoardService = Depends(),
) -> BoardsListResponse:
    objs = await service.get_boards()
    return BoardsListResponse(
        payload=[BoardDB.model_validate(obj) for obj in objs]
    )


@router.patch("/{obj_id}")
async def update(
        obj_id: UUID4,
        data: UpdateBoardRequest,
        service: BoardService = Depends(),
) -> BoardResponse:
    obj = await service.update_board(
        obj_id,
        data.model_dump(exclude_unset=True),
    )
    return BoardResponse(payload=BoardDB.model_validate(obj))


@router.delete("/{obj_id}")
async def delete(
        obj_id: UUID4,
        service: BoardService = Depends(),
) -> None:
    await service.delete_board(obj_id)
