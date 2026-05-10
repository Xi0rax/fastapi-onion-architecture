from uuid import UUID

from src.models import SprintModel
from src.utils.constans import SPRINT_NOT_FOUND_MSG
from src.utils.service import BaseService


class SprintService(BaseService):
    _repo = "sprint"

    async def create_sprint(self, data: dict) -> SprintModel:
        return await self.add_one_and_get_obj(**data)

    async def get_sprint(self, obj_id: UUID) -> SprintModel:
        obj = await self.get_by_filter_one_or_none(id=obj_id)
        self.check_existence(obj, SPRINT_NOT_FOUND_MSG)
        return obj

    async def get_sprints(self):
        return await self.get_by_filter_all()

    async def update_sprint(self, obj_id: UUID, data: dict):
        obj = await self.update_one_by_id(obj_id, **data)
        self.check_existence(obj, SPRINT_NOT_FOUND_MSG)
        return obj

    async def delete_sprint(self, obj_id: UUID):
        await self.delete_by_ids(obj_id)
