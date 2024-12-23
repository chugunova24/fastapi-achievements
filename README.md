Разработка API для работы с достижениями
==============
▄█▀ ▀█▀ ▄▀▄ █▀ █▄█▄█ ▄▀▄ █▀ ▄█▀
## Стек технологий
1. Веб-фреймворк: FastAPI 0.115.6
2. ORM: SQLAlchemy 2.0.36
3. СУБД: PostgreSQL 17
4. Управление миграциями: Alembic 1.14.0
3. Сериализация/Десериализация: Pydantic
3. Тестирование: Pytest 8.3.4

## Первые шаги:
Склонируйте репозиторий:

```bash
git clone https://github.com/chugunova24/fastapi-achievements.git
```

Зайдите в папку проекта:

```bash
cd fastapi-achievements
```

Разверните контейнеры посредством Docker:

```bash
make compose
```
или
```bash
docker compose up --build
```

**После запуска всех контейнеров, в браузере пройдите по ссылке**:
```
http://0.0.0.0/docs
```
- - - ─╤╦︻--(°□°╯)[̲̅П̲̅][̲̅о̲̅][̲̅р̲̅][̲̅в̲̅][̲̅у̲̅] [̲̅З̲̅][̲̅а̲̅] [̲̅Д̲̅][̲̅р̲̅][̲̅у̲̅][̲̅з̲̅][̲̅е̲̅][̲̅й̲̅](╯°□°)--︻╦╤─ - - -
## Адреса серверов
| #       | Адрес сервера | 
|---------|---------------|
| FastAPI | 0.0.0.0:8001  |
| NGINX   | 0.0.0.0:80    |

## Запуск тестов
Подключитесь к контейнеру с fastapi приложением:
```bash
docker exec -itu root app /bin/bash 
```
Выполните команду:
```bash
make run-tests
```