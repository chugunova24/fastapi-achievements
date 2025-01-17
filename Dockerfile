# Используем официальный образ Python 3.12 как базовый
FROM python:3.12-slim as base

# Устанавливаем переменные окружения для предотвращения взаимодействия с интерактивным режимом
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем необходимые пакеты и инструменты для Poetry и установки зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry 1.8.4
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.4

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:${PATH}"

# Рабочий каталог внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости проекта
RUN poetry install --no-dev --no-interaction --no-root

# Копируем оставшиеся файлы проекта
COPY . /app/

# Порт для приложения FastAPI
EXPOSE 8001

# Запускаем приложение
ENTRYPOINT ["scripts/entry-point.sh"]