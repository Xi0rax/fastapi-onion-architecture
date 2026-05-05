from sqlalchemy import delete

from task.src.models import TaskWatcherModel
from task.src.utils.repository import SqlAlchemyRepository


class TaskWatcherRepository(SqlAlchemyRepository[TaskWatcherModel]):
    _model = TaskWatcherModel

    async def delete_by_filter(self, task_id, user_id):
        query = delete(self._model).where(
            self._model.task_id == task_id,
            self._model.user_id == user_id,
        )
        await self._session.execute(query)