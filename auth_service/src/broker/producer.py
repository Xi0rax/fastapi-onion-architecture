import json

import aio_pika

from auth_service.src.config import settings


class RabbitProducer:
    def __init__(self, channel=None):
        self.channel = channel

    async def publish(self, queue: str, message: dict):
        if self.channel is not None:
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode()
                ),
                routing_key=queue,
            )
            return

        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        try:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message).encode()),
                routing_key=queue,
            )
        finally:
            await connection.close()
