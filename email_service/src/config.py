import os

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(".env"))


def _getenv(name: str, default: str) -> str:
    return os.getenv(name, default)


class Settings:
    APP_NAME: str = "email_service-service"

    RABBITMQ_HOST: str = _getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT: int = int(_getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_USER: str = _getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = _getenv("RABBITMQ_PASSWORD", "guest")
    NOTIFICATION_QUEUE: str = _getenv("NOTIFICATION_QUEUE", "email.notifications")

    @property
    def RABBITMQ_URL(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )


settings = Settings()
