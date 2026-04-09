from src.utils.service import BaseService, transaction_mode


class TaskExecutorService(BaseService):
    _repo = "task_executor"

    async def add_executor(self, task_id, user_id):
        await self.add_one(task_id=task_id, user_id=user_id)

    @transaction_mode
    async def remove_executor(self, task_id, user_id):
        await self.uow.task_executor.delete_by_filter(
            task_id=task_id,
            user_id=user_id,
        )
