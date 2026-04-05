from uuid import UUID

from src.models import ColumnModel
from src.utils.constans import COLUMN_NOT_FOUND_MSG
from src.utils.service import BaseService


class ColumnService(BaseService):
    _repo = "column"

    async def create_column(self, data: dict) -> ColumnModel:
        return await self.add_one_and_get_obj(**data)

    async def get_column(self, obj_id: UUID) -> ColumnModel:
        obj = await self.get_by_filter_one_or_none(id=obj_id)
        self.check_existence(obj, COLUMN_NOT_FOUND_MSG)
        return obj

    async def get_columns(self):
        return await self.get_by_filter_all()

    async def update_column(self, obj_id: UUID, data: dict):
        obj = await self.update_one_by_id(obj_id, **data)
        self.check_existence(obj, COLUMN_NOT_FOUND_MSG)
        return obj

    async def delete_column(self, obj_id: UUID):
        await self.delete_by_ids(obj_id)
