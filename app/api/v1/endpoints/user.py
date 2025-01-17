from fastapi import APIRouter
from starlette import status

from app.db.session import SessionDep
from app.schemas import user_schemas, achievement_schemas
from app.services import user as user_repo

router = APIRouter()


@router.post("/",
             response_model=user_schemas.User,
             status_code=status.HTTP_201_CREATED)
def create_user(
        user: user_schemas.UserCreate,
        db: SessionDep
):
    """
    Создание нового пользователя в системе.

    Этот эндпоинт добавляет нового пользователя
    в базу данных на основе предоставленных данных.

    **Параметры**:
    - `user` (UserCreate): Объект, содержащий данные
    для создания пользователя. Поля:
      - `name`: Имя пользователя (обязательное).
      - `language`: Предпочитаемый язык пользователя (по умолчанию — "en").
    - `db` (Session): Текущая сессия базы данных.

    **Возвращаемое значение**:
    - Объект `User`, представляющий созданного пользователя, с полями:
      - `id`: Уникальный идентификатор пользователя.
      - `name`: Имя пользователя.
      - `language`: Язык пользователя.

    **Пример запроса**:
    ```
    POST /users/

    {
      "name": "John Doe",
      "language": "en"
    }
    ```

    **Пример ответа**:
    ```
    {
      "id": 1,
      "name": "John Doe",
      "language": "en"
    }
    ```

    **Возвращаемые статусы**:
    - HTTP 201 (Created): Пользователь успешно создан.
    - HTTP 422 (Validation Error): Неверные данные для создания пользователя.
    """
    return user_repo.create_user(db=db, user=user)


@router.post("/{user_id}/achievements",
             response_model=achievement_schemas.UserAchievementsOut,
             status_code=status.HTTP_201_CREATED)
def issue_achievement(
        user_id: int,
        user_achievement: user_schemas.UserAchievementCreate,
        db: SessionDep
):
    """
    Выдача достижения пользователю.

    Этот эндпоинт позволяет добавить новое
    достижение пользователю.

    **Параметры пути**:
    - `user_id` (int): Уникальный идентификатор
    пользователя, которому нужно выдать достижение.

    **Тело запроса**:
    - Объект `UserAchievementCreate`, содержащий следующие поля:
      - `achievement_id` (int): Уникальный идентификатор достижения.

    **Возвращаемое значение**:
    - Объект `UserAchievementsOut`, содержащий
    информацию о выданном достижении, включая:
      - `user_id` (int): Уникальный идентификатор пользователя.
      - `achievement_id` (int): Уникальный идентификатор достижения.
      - `timestamp` (datetime): Время выдачи достижения.

    **Пример запроса**:
    ```
    POST /users/11/achievements
    Content-Type: application/json

    {
        "achievement_id": 22,
    }
    ```
    **Пример ответа**:
    ```
    HTTP/1.1 201 Created
    Content-Type: application/json

    {
      "user_id": 11,
      "achievements": [
        {
          "id": 22,
          "name": "Мастер",
          "description": "Заверши уровень мастера",
          "points": 100,
          "issued_at": "2024-12-23T12:04:21.126139"
        }
      ]
    }
    ```
    **Возвращаемый статус**:
    - HTTP 201 (Created): Достижение успешно выдано.
    - HTTP 404 (Not Found): Пользователь или достижение не найдены.
    - HTTP 422 (Validation Error): Неверные данные для создания достижения.
    """
    return user_repo.issue_achievement(
        user_id=user_id,
        db=db,
        user_achievement=user_achievement
    )


@router.get("/",
            response_model=list[user_schemas.User],
            status_code=status.HTTP_200_OK)
def read_users(db: SessionDep):
    """
    Получение списка всех пользователей сервиса.

    Этот эндпоинт возвращает список всех
    пользователей, зарегистрированных в системе.

    **Возвращаемое значение**:
    - Список объектов `User`, которые имеют следующие поля:
        - `id`: Идентификатор пользователя.
        - `name`: Имя пользователя.
        - `language`: Язык пользователя.

    **Пример запроса**:
    ```
    GET /users/{user_id}/achievements
    ```

    **Пример ответа**:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
      {
        "id": "1",
        "name": "John",
        "language": "ru"
      },
      {
        "id": "2",
        "name": "Alice",
        "language": "en"
      }
    ]
    ```
    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    """
    return user_repo.get_users(db=db)


@router.get("/{user_id}/achievements",
            response_model=achievement_schemas.UserAchievementsOut)
def get_user_achievements(
        user_id: int,
        db: SessionDep
):
    """
    Получение всех достижений пользователя по его
    идентификатору.

    Этот эндпоинт возвращает список достижений,
    связанных с указанным пользователем.
    Достижения представляют собой набор данных,
    которые показывают, каких успехов
    достиг пользователь в приложении.

    **Параметры пути**:
    - `user_id` (int): Уникальный идентификатор
    пользователя.

    **Возвращаемое значение**:
    - Объект `UserAchievementsOut`, который содержит следующие поля:
      - `user_id`: Уникальный идентификатор пользователя.
      - `achievements`: Список достижений пользователя, имеет следующие поля:
        - `id`: ID достижения.
        - `name`: Название достижения.
        - `description`: Описание достижения.
        - `points`: Сколько очков дает пользователю достижение.
        - `issued_at`: Дата и время выдачи достижения пользователю.

    **Пример запроса**:
    ```
    GET /users/1/achievements
    ```

    **Пример ответа**:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "user_id": 1,
      "achievements": [
        {
          "id": 1,
          "name": "First Steps",
          "description": "Your first achievement",
          "points": 10,
          "issued_at": "2024-12-23T12:42:10.844907"
        },
        {
          "id": 2,
          "name": "Master",
          "description": "Complete the master lvl",
          "points": 100,
          "issued_at": "2024-12-23T13:24:16.378711"
        }
      ]
    }
    ```

    **Возвращаемый статус**:
    - HTTP 200 (OK) при успешном выполнении запроса.
    - HTTP 404 (Not Found): Пользователь или достижение не найдены.
    """
    return user_repo.get_user_achievements(
        user_id=user_id,
        db=db
    )
