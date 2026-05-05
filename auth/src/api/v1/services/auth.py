from fastapi import Depends, HTTPException

from auth.src.broker.producer import RabbitProducer
from auth.src.broker.task_stats_client import TaskStatsClient
from auth.src.schemas.auth import RegisterRequest, LoginRequest
from auth.src.security.jwt import create_access_token
from auth.src.security.password import hash_password, verify_password
from auth.src.utils.base_service import BaseService, transaction_mode


class AuthService(BaseService):
    _repo = "user"

    def __init__(
        self,
        producer: RabbitProducer = Depends(),
        task_stats_client: TaskStatsClient = Depends(),
        **kwargs,
    ):
        super().__init__(**kwargs)
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
        user = await self.get_by_filter_one_or_none(id=user_id)

        self.check_existence(user, "User not found")

        stats = await self.task_stats_client.get_user_task_stats(str(user.id))

        return {
            **user.__dict__,
            **stats,
        }