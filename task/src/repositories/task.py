from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.engine import Result

from src.models import TaskModel
from src.schemas.task import TaskFilters
from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository[TaskModel]):
    _model = TaskModel

    async def get_tasks_by_filter(self, filters: TaskFilters) -> Sequence[TaskModel]:
        query = select(self._model)

        if filters.ids:
            query = query.where(self._model.id.in_(filters.ids))

        if filters.author_id:
            query = query.where(self._model.author_id.in_(filters.author_id))

        if filters.assignee_id:
            query = query.where(self._model.assignee_id.in_(filters.assignee_id))

        if filters.status:
            query = query.where(self._model.status.in_(filters.status))

        if filters.like:
            query = query.where(self._model.title.ilike(f"%{filters.like}%"))

        if filters.limit:
            query = query.limit(filters.limit).offset(filters.offset)

        res: Result = await self._session.execute(query)
        return res.scalars().all()