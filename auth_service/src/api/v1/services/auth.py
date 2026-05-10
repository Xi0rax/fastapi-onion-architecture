from fastapi import Depends, HTTPException

from auth_service.src.broker.producer import RabbitProducer
from auth_service.src.broker.task_stats_client import TaskStatsClient
from auth_service.src.schemas.auth import RegisterRequest, LoginRequest
from auth_service.src.security.jwt_utils import create_access_token
from auth_service.src.security.password import hash_password, verify_password
from auth_service.src.utils.service import BaseService, transaction_mode
from auth_service.src.utils.unit_of_work import UnitOfWork


class AuthService(BaseService):
    _repo = "user"

    def __init__(
            self,
            uow: UnitOfWork = Depends(),
            producer: RabbitProducer = Depends(),
            task_stats_client: TaskStatsClient = Depends(),
    ) -> None:
        super().__init__(uow=uow)
        self.producer = producer
        self.task_stats_client = task_stats_client

    @transaction_mode
    async def register(self, data: RegisterRequest):
        existing = await self.get_by_filter_one_or_none(email=data.email)

        if existing:
            raise HTTPException(400, "User already exists")

        user = await self.add_one_and_get_obj(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
        )

        await self.producer.publish(
            "email.notifications",
            {
                "type": "user_registered",
                "data": {
                    "user_id": str(user.id),
                    "email": user.email,
                },
            },
        )

        return user

    async def login(self, data: LoginRequest):
        user = await self.get_by_filter_one_or_none(email=data.email)

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(401, "Invalid credentials")

        return create_access_token(str(user.id))

    async def get_user_info(self, user_id):
        user = await self.get_user_profile(user_id)

        stats = await self.task_stats_client.get_user_task_stats(str(user.id))

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            **stats,
        }

    async def get_user_profile(self, user_id):
        user = await self.get_by_filter_one_or_none(id=user_id)
        self.check_existence(user, "User not found")
        return user
