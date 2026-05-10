import json
from typing import Any

import aio_pika

from src.api.v1.services.auth import AuthService
from src.utils.unit_of_work import UnitOfWork


class UserInfoRpcConsumer:
    def __init__(self, service: AuthService | None = None) -> None:
        self.service = service or AuthService(uow=UnitOfWork())

    async def handle_payload(self, payload: dict[str, Any]) -> dict[str, str]:
        user = await self.service.get_user_profile(payload["user_id"])
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
        }

    async def handle_message(self, message: aio_pika.IncomingMessage) -> None:
        async with message.process():
            payload = json.loads(message.body.decode())
            response = await self.handle_payload(payload)

            if message.reply_to:
                await message.channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(response).encode(),
                        correlation_id=message.correlation_id,
                    ),
                    routing_key=message.reply_to,
                )
