import os
from contextlib import asynccontextmanager

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from task_service.src.api import router
from task_service.src.broker import TaskStatsRpcConsumer, get_channel
from task_service.src.config import settings
from task_service.src.database import create_db_tables
from task_service.src.metadata import DESCRIPTION, TAG_METADATA, TITLE, VERSION


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    connection = None
    try:
        await create_db_tables()
        connection, channel = await get_channel()
        queue = await channel.declare_queue(settings.TASK_STATS_QUEUE, durable=True)
        await queue.consume(TaskStatsRpcConsumer().handle_message)
        fastapi_app.state.rabbitmq_connection = connection
    except Exception:
        fastapi_app.state.rabbitmq_connection = None

    yield

    if connection:
        await connection.close()


def create_fast_api_app() -> FastAPI:
    load_dotenv(find_dotenv('.env'))
    env_name = os.getenv('MODE', 'DEV')

    if env_name != 'PROD':
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            lifespan=lifespan,
        )
    else:
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            lifespan=lifespan,
            docs_url=None,
            redoc_url=None,
        )

    fastapi_app.include_router(router, prefix='/api')
    return fastapi_app


app = create_fast_api_app()
