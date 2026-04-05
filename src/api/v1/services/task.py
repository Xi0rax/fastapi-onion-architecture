from typing import Sequence
from uuid import UUID

from src.models import TaskModel
from src.schemas.task import TaskFilters
from src.utils.constans import TASK_NOT_FOUND_MSG
from src.utils.service import BaseService


class TaskService(BaseService):
    _repo = "task"

    async def create_task(self, data: dict) -> TaskModel:
        return await self.add_one_and_get_obj(**data)

    async def get_task(self, task_id: UUID) -> TaskModel:
        task = await self.get_by_filter_one_or_none(id=task_id)
        self.check_existence(task, TASK_NOT_FOUND_MSG)
        return task

    async def get_tasks(self, filters: TaskFilters) -> Sequence[TaskModel]:
        return await self.uow.task.get_tasks_by_filter(filters)

    async def update_task(self, task_id: UUID, data: dict) -> TaskModel:
        task = await self.update_one_by_id(task_id, **data)
        self.check_existence(task, TASK_NOT_FOUND_MSG)
        return task

    async def delete_task(self, task_id: UUID) -> None:
        await self.delete_by_ids(task_id)
