import logging
import time
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import api_router
from app.db.session import get_db
from app.db.utils import init_db


# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Создание middleware для логгирования
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Логирование запроса
        logger.info(f"Request: {request.method} {request.url}")

        # Обработка запроса и получение ответа
        response = await call_next(request)

        # Логирование ответа
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} | Processing time: {process_time:.4f}s")

        return response


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db = next(get_db())
    init_db(db)  # Инициализация данных при старте
    yield


app = FastAPI(
    lifespan=lifespan
)


# Добавление middleware
app.add_middleware(LoggingMiddleware)


@app.get("/")
def ping():
    return {"message": "pong!"}


# Подключение эндпоинтов
app.include_router(api_router)
