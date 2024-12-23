#!/bin/bash

# Остановить выполнение при ошибке
set -e

echo "Starting FastAPI application..."
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8001 &
UVICORN_PID=$!

# Обработка сигналов
trap "kill $UVICORN_PID" SIGTERM SIGINT

# Ожидание завершения процессов
wait $UVICORN_PID
