import aio_pika

from task_service.src.config import settings


async def get_channel():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    return connection, channel
