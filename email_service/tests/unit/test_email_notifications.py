from unittest.mock import AsyncMock

import pytest

from email_service.src.consumers.email_notifications import EmailNotificationConsumer


@pytest.mark.asyncio
async def test_user_registered_event_sends_notification():
    service = AsyncMock()
    consumer = EmailNotificationConsumer(service=service)

    await consumer.handle_payload(
        {
            "type": "user_registered",
            "data": {
                "user_id": "user-1",
                "email": "user@example.com",
            },
        }
    )

    service.send_user_registered.assert_awaited_once_with(user_id="user-1", email="user@example.com")


@pytest.mark.asyncio
async def test_unknown_event_is_ignored():
    service = AsyncMock()
    consumer = EmailNotificationConsumer(service=service)

    await consumer.handle_payload({"type": "unknown", "data": {}})

    service.send_user_registered.assert_not_called()
