import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))


def _getenv(name: str, default: str) -> str:
    return os.getenv(name, default)


class Settings:
    MODE: str = _getenv('MODE', 'DEV')

    DB_HOST: str = _getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(_getenv('DB_PORT', '5432'))
    DB_USER: str = _getenv('DB_USER', 'postgres')
    DB_PASS: str = _getenv('DB_PASS', 'postgres')
    DB_NAME: str = _getenv('DB_NAME', 'dev_db')

    DB_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    RABBITMQ_HOST: str = _getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT: int = int(_getenv('RABBITMQ_PORT', '5672'))
    RABBITMQ_USER: str = _getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD: str = _getenv('RABBITMQ_PASSWORD', 'guest')
    TASK_STATS_QUEUE: str = _getenv('TASK_STATS_QUEUE', 'task_service.user_stats')
    AUTH_USER_INFO_QUEUE: str = _getenv('AUTH_USER_INFO_QUEUE', 'auth_service.user_info')

    RABBITMQ_URL: str = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/'


settings = Settings()
