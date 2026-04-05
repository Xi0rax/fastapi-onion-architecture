from src.utils.service import BaseService


class TaskWatcherService(BaseService):
    _repo = "task_watcher"

    async def add_watcher(self, task_id, user_id):
        await self.add_one(task_id=task_id, user_id=user_id)

    async def remove_watcher(self, task_id, user_id):
        await self.uow.task_watcher.delete_by_filter(
            task_id=task_id,
            user_id=user_id,
        )
