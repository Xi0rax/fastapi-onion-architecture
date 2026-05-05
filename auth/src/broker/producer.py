import json

import aio_pika


class RabbitProducer:
    def __init__(self, channel):
        self.channel = channel

    async def publish(self, queue: str, message: dict):
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode()
            ),
            routing_key=queue,
        )
