#!/bin/bash

# Проверяем, передан ли аргумент
if [ -z "$1" ]; then
  echo "Ошибка: необходимо указать сообщение для ревизии."
  echo "Использование: $0 \"<message>\""
  exit 1
fi

MESSAGE="$1"

# Выполняем команду и проверяем её успешность
if poetry run alembic revision --autogenerate -m "$MESSAGE"; then
  echo "Ревизия успешно создана с сообщением: $MESSAGE"
else
  echo "Произошла ошибка при создании ревизии."
  exit 1
fi
