import json
from collections.abc import Awaitable, Callable
from typing import Any

from loguru import logger

from email_service.src.services.email import EmailNotificationService


class EmailNotificationConsumer:
    def __init__(self, service: EmailNotificationService | None = None) -> None:
        self.service = service or EmailNotificationService()

    async def handle_payload(self, payload: dict[str, Any]) -> None:
        event_type = payload.get("type")
        data = payload.get("data") or {}

        if event_type == "user_registered":
            await self.service.send_user_registered(
                user_id=str(data["user_id"]),
                email=str(data["email"]),
            )
            return

        logger.warning("Unknown email_service event type: {}", event_type)

    async def handle_message(self, message: Any) -> None:
        async with message.process():
            payload = json.loads(message.body.decode())
            await self.handle_payload(payload)


async def consume(queue: Any, handler: Callable[[Any], Awaitable[None]] | None = None) -> None:
    consumer = EmailNotificationConsumer()
    await queue.consume(handler or consumer.handle_message)
