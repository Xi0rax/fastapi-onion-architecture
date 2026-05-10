from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from auth_service.src.api import router
from auth_service.src.api.v1.routers import v1_auth_router
from auth_service.src.broker import UserInfoRpcConsumer, get_channel
from auth_service.src.config import settings
from auth_service.src.database import create_db_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = None
    try:
        await create_db_tables()
        connection, channel = await get_channel()
        queue = await channel.declare_queue(settings.AUTH_USER_INFO_QUEUE, durable=True)
        await queue.consume(UserInfoRpcConsumer().handle_message)
        app.state.rabbitmq_connection = connection
    except Exception:
        app.state.rabbitmq_connection = None

    yield

    if connection:
        await connection.close()


def create_fast_api_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    app.include_router(router, prefix="/api")
    app.include_router(v1_auth_router)
    return app


app = create_fast_api_app()
