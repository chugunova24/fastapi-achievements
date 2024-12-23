from fastapi import APIRouter

from app.db.session import SessionDep
from app.schemas import achievement_schemas
from app.services import achievement as achievement_repo


router = APIRouter()


@router.post("/",
             response_model=achievement_schemas.Achievement)
def create_achievement(
        achievement: achievement_schemas.AchievementCreate,
        db: SessionDep
):
    """
    Создание нового достижения.

    Этот эндпоинт позволяет создать новое достижение в системе.

    **Параметры пути**:
    Отсутствуют

    **Возвращаемое значение**:
    - Объект `AchievementCreate`, содержащий следующие поля:
      - `id` (int): Идентификатор достижения.
      - `name_en` (str): Название достижения на английском языке.
      - `name_ru` (str): Название достижения на русском языке.
      - `points` (int): Количество очков, которые начисляют за достижение.
      - `description_en` (str): Описание достижения на английском языке.
      - `description_ru` (str): Описание достижения на русском языке.

    **Пример запроса**:
    ```
    POST /achievements
    ```

    **Пример ответа**:
    ```
    HTTP/1.1 201 Created
    Content-Type: application/json

    {
      "id": 1,
      "name_ru": "Мастер",
      "points": 10,
      "description_en": "You are master",
      "description_ru": "Ты мастер"
    }
    ```

    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    - HTTP 422 (Validation Error): Неверные данные для создания достижения.
    """
    return achievement_repo.create_achievement(
        db=db,
        achievement=achievement
    )


@router.get("/",
            response_model=list[achievement_schemas.Achievement])
def read_achievements(db: SessionDep):
    """
    Получение списка всех достижений в системе.

    Этот эндпоинт позволяет получить список всех существующих в базе данных
    достижений.

    **Параметры пути**:
    Отсутствуют

    **Возвращаемое значение**:
    - Список объектов `Achievement`, содержащий следующие поля:
      - `id` (int): Идентификатор достижения.
      - `name_en` (str): Название достижения на английском языке.
      - `name_ru` (str): Название достижения на русском языке.
      - `points` (int): Количество очков, которые начисляют за достижение.
      - `description_en` (str): Описание достижения на английском языке.
      - `description_ru` (str): Описание достижения на русском языке.

    **Пример запроса**:
    ```
    GET /achievements
    ```

    **Пример ответа**:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
        {
            "id": 1,
            "name_en": "Master",
            "name_ru": "Мастер",
            "points": 10,
            "description_en": "You are master",
            "description_ru": "Ты мастер"
        }
    ]
    ```

    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    """
    return achievement_repo.get_achievements(db=db)


@router.get("/stats/top-user")
def get_user_with_max_achievements(db: SessionDep):
    """
    Извлечь пользователя(ей) с максимальным количеством достижений.

    Этот эндпоинт возвращает пользователя(ей), заработавшего наибольшее количество достижений.
    Вычисляет пользователя(ей) с наибольшим количеством достижений и возвращает их данные,
    такие как идентификатор пользователя, имя и количество достижений.

    **Параметры запроса**:
    - Отсутствуют.

    **Возвращаемое значение**:
    - Список словарей, состоящих из следующих полей:
      - `user_id` (int): Уникальный идентификатор пользователя.
      - `user_name` (str): Имя пользователя.
      - `achievement_count` (int): Количество достижений пользователя.

    **Пример запроса**:
    ```
    GET /achievements/stats/top-user
    ```
    **Пример ответа**:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
      {
        "user_id": 3,
        "user_name": "Alice",
        "achievement_count": 2
      }
    ]
    ```
    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    """
    return achievement_repo.users_with_max_achievements(db=db)


@router.get("/stats/top-user-points")
def get_user_with_max_points(db: SessionDep):
    """
    Извлечь пользователя(ей) с максимальным количеством очков.

    Этот эндпоинт возвращает пользователя(ей), заработавшего наибольшее количество очков.
    Вычисляет пользователя(ей) с наибольшим количеством очков и возвращает их данные,
    такие как идентификатор пользователя, имя и количество достижений.

    **Параметры запроса**:
    - Отсутствуют.

    **Возвращаемое значение**:
    - Список словарей, состоящих из следующих полей:
      - `user_id` (int): Уникальный идентификатор пользователя.
      - `user_name` (str): Имя пользователя.
      - `total_points` (int): Количество очков пользователя.

    **Пример запроса**:
    ```
    GET /achievements/stats/top-user-points
    ```
    **Пример ответа**:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
      {
        "user_id": 3,
        "user_name": "Alice",
        "total_points": 110
      }
    ]
    ```
    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    """
    return achievement_repo.user_with_max_points(db=db)


@router.get("/stats/max-points-difference")
def get_users_with_max_points_difference(db: SessionDep):
    """
    Извлечь пользователей с максимальной разностью очков
    достижений (разность баллов между  пользователями).

    **Параметры запроса**:
    - Отсутствуют.

    **Возвращаемое значение**:
    - Список парных словарей, состоящих из следующих полей:
      - `user_1` (int): Данные о первом пользователе.
      - `user_2` (int):  Данные о втором пользователе.
      - `id` (int): Уникальный идентификатор пользователя.
      - `name` (str): Имя пользователя.
      - `total_points` (int): Количество очков пользователя.
      - `points_difference` (int): Разница очков двух пользователей.

    **Пример запроса**:
    ```
    GET /achievements/stats/max-points-difference
    ```
    **Пример ответа**:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
      {
        "user_1": {
          "id": 2,
          "name": "Maria",
          "total_points": 100
        },
        "user_2": {
          "id": 3,
          "name": "Alice",
          "total_points": 110
        },
        "points_difference": 10
      }
    ]
    ```
    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    """
    return achievement_repo.get_users_with_points_difference(
        db=db,
        find_max=True
    )

@router.get("/stats/min-points-difference")
def get_users_with_min_points_difference(db: SessionDep):
    """
    Извлечь пользователей с минимальной разностью очков
    достижений (разность баллов между пользователями).

    **Параметры запроса**:
    - Отсутствуют.

    **Возвращаемое значение**:
    - Список парных словарей, состоящих из следующих полей:
      - `user_1` (int): Данные о первом пользователе.
      - `user_2` (int):  Данные о втором пользователе.
      - `id` (int): Уникальный идентификатор пользователя.
      - `name` (str): Имя пользователя.
      - `total_points` (int): Количество очков пользователя.
      - `points_difference` (int): Разница очков двух пользователей.

    **Пример запроса**:
    ```
    GET /achievements/stats/min-points-difference
    ```
    **Пример ответа**:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
      {
        "user_1": {
          "id": 2,
          "name": "Maria",
          "total_points": 100
        },
        "user_2": {
          "id": 3,
          "name": "Alice",
          "total_points": 110
        },
        "points_difference": 10
      }
    ]
    ```
    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    """
    return achievement_repo.get_users_with_points_difference(
        db=db,
        find_max=False
    )


@router.get("/stats/7-day-streak")
def get_users_with_7_day_streak(db: SessionDep):
    """
    Извлечь пользователей, которые получали достижения 7 дней подряд
    (по дате выдачи, хотя бы  одно в каждый из 7 дней)

    **Параметры запроса**:
    - Отсутствуют.

    **Возвращаемое значение**:
    - Список парных словарей, состоящих из следующих полей:
      - `user_1` (int): Данные о первом пользователе.
      - `user_2` (int):  Данные о втором пользователе.
      - `id` (int): Уникальный идентификатор пользователя.
      - `name` (str): Имя пользователя.
      - `total_points` (int): Количество очков пользователя.
      - `points_difference` (int): Разница очков двух пользователей.

    **Пример запроса**:
    ```
    GET /achievements/stats/7_day_streak
    ```
    **Пример ответа**:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
        1,
        34,
        9
    ]
    ```
    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    """
    return achievement_repo.users_with_7_day_streak(
        db=db
    )