from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.engine import Result

from task.src.models import UserModel
from task.src.schemas.user import UserFilters
from task.src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[UserModel]):
    _model = UserModel

    async def get_users_by_filter(self, filters: UserFilters) -> Sequence[UserModel]:
        query = select(self._model)

        if filters.ids:
            query = query.where(self._model.id.in_(filters.ids))

        if filters.full_name:
            query = query.where(self._model.full_name.in_(filters.full_name))

        if filters.email:
            query = query.where(self._model.email.in_(filters.email))

        if filters.like:
            query = query.where(self._model.full_name.ilike(f"%{filters.like}%"))

        if filters.limit:
            query = query.limit(filters.limit).offset(filters.offset)

        res: Result = await self._session.execute(query)
        return res.scalars().all()