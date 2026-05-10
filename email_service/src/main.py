from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from email_service.src.broker import get_channel
from email_service.src.config import settings
from email_service.src.consumers import consume


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = None
    try:
        connection, channel = await get_channel()
        queue = await channel.declare_queue(settings.NOTIFICATION_QUEUE, durable=True)
        await consume(queue)
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

    @app.get("/healthz/")
    async def health_check() -> dict[str, bool]:
        return {"ok": True}

    return app


app = create_fast_api_app()
