from loguru import logger


class EmailNotificationService:
    async def send_user_registered(self, user_id: str, email: str) -> None:
        logger.info("User registration email_service prepared for user_id={} email={}", user_id, email)
