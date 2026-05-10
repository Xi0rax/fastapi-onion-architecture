import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))


def _getenv(name: str, default: str) -> str:
    return os.getenv(name, default)


class Settings:
    APP_NAME: str = "auth_service-service"
    DEBUG: bool = _getenv("DEBUG", "false").lower() == "true"

    DB_HOST: str = _getenv("DB_HOST", "localhost")
    DB_PORT: int = int(_getenv("DB_PORT", "5432"))
    DB_NAME: str = _getenv("DB_NAME", "auth_db")
    DB_USER: str = _getenv("DB_USER", "postgres")
    DB_PASSWORD: str = _getenv("DB_PASSWORD", "postgres")

    JWT_SECRET: str = _getenv("JWT_SECRET", "change-me-in-production-change-me")
    JWT_ALGORITHM: str = _getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_HOURS: int = int(_getenv("JWT_EXPIRE_HOURS", "24"))

    RABBITMQ_HOST: str = _getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT: int = int(_getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_USER: str = _getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = _getenv("RABBITMQ_PASSWORD", "guest")
    TASK_STATS_QUEUE: str = _getenv("TASK_STATS_QUEUE", "task_service.user_stats")
    AUTH_USER_INFO_QUEUE: str = _getenv("AUTH_USER_INFO_QUEUE", "auth_service.user_info")

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def RABBITMQ_URL(self) -> str:
        return (
            f"amqp://"
            f"{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )


settings = Settings()
