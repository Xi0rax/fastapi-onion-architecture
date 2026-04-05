from uuid import UUID

from src.models import BoardModel
from src.utils.constans import BOARD_NOT_FOUND_MSG
from src.utils.service import BaseService


class BoardService(BaseService):
    _repo = "board"

    async def create_board(self, data: dict) -> BoardModel:
        return await self.add_one_and_get_obj(**data)

    async def get_board(self, obj_id: UUID) -> BoardModel:
        obj = await self.get_by_filter_one_or_none(id=obj_id)
        self.check_existence(obj, BOARD_NOT_FOUND_MSG)
        return obj

    async def get_boards(self):
        return await self.get_by_filter_all()

    async def update_board(self, obj_id: UUID, data: dict):
        obj = await self.update_one_by_id(obj_id, **data)
        self.check_existence(obj, BOARD_NOT_FOUND_MSG)
        return obj

    async def delete_board(self, obj_id: UUID):
        await self.delete_by_ids(obj_id)
