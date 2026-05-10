import json
from typing import Any
from uuid import UUID

import aio_pika

from task_service.src.api.v1.services.task import TaskService
from task_service.src.utils.unit_of_work import UnitOfWork


class TaskStatsRpcConsumer:
    def __init__(self, service: TaskService | None = None) -> None:
        self.service = service or TaskService(uow=UnitOfWork())

    async def handle_payload(self, payload: dict[str, Any]) -> dict[str, int]:
        user_id = UUID(str(payload['user_id']))
        return await self.service.get_user_task_stats(user_id)

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
