import asyncio
import json
from uuid import uuid4

import aio_pika

from task_service.src.config import settings


class AuthUserClient:
    async def get_user_info(self, user_id: str) -> dict:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        try:
            channel = await connection.channel()
            callback_queue = await channel.declare_queue(exclusive=True)
            correlation_id = str(uuid4())
            future = asyncio.get_running_loop().create_future()

            async def on_response(message: aio_pika.IncomingMessage) -> None:
                if message.correlation_id == correlation_id:
                    future.set_result(json.loads(message.body.decode()))

            await callback_queue.consume(on_response, no_ack=True)
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps({"user_id": user_id}).encode(),
                    correlation_id=correlation_id,
                    reply_to=callback_queue.name,
                ),
                routing_key=settings.AUTH_USER_INFO_QUEUE,
            )
            return await asyncio.wait_for(future, timeout=5)
        finally:
            await connection.close()
