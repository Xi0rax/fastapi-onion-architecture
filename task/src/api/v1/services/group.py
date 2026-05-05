from uuid import UUID

from src.models import GroupModel
from src.utils.constans import GROUP_NOT_FOUND_MSG
from src.utils.service import BaseService


class GroupService(BaseService):
    _repo = "group"

    async def create_group(self, data: dict) -> GroupModel:
        return await self.add_one_and_get_obj(**data)

    async def get_group(self, obj_id: UUID) -> GroupModel:
        obj = await self.get_by_filter_one_or_none(id=obj_id)
        self.check_existence(obj, GROUP_NOT_FOUND_MSG)
        return obj

    async def get_groups(self):
        return await self.get_by_filter_all()

    async def update_group(self, obj_id: UUID, data: dict):
        obj = await self.update_one_by_id(obj_id, **data)
        self.check_existence(obj, GROUP_NOT_FOUND_MSG)
        return obj

    async def delete_group(self, obj_id: UUID):
        await self.delete_by_ids(obj_id)
