from uuid import UUID
from typing import Sequence

from src.utils.service import BaseService
from src.schemas.user import UserFilters, UserDB
from src.models import UserModel


class UserService(BaseService):
    _repo = "user"

    async def create_user(self, data: dict) -> UserModel:
        return await self.add_one_and_get_obj(**data)

    async def get_user(self, user_id: UUID) -> UserModel:
        user = await self.get_by_filter_one_or_none(id=user_id)
        self.check_existence(user, "User not found")
        return user

    async def get_users(self, filters: UserFilters) -> Sequence[UserModel]:
        return await self.uow.user.get_users_by_filter(filters)

    async def update_user(self, user_id: UUID, data: dict) -> UserModel:
        user = await self.update_one_by_id(user_id, **data)
        self.check_existence(user, "User not found")
        return user

    async def delete_user(self, user_id: UUID) -> None:
        await self.delete_by_ids(user_id)