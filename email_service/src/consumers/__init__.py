__all__ = [
    "EmailNotificationConsumer",
    "consume",
]

from email_service.src.consumers.email_notifications import EmailNotificationConsumer, consume
