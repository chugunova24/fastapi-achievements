from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, over, Integer

from app.models.achievement import Achievement
from app.models.user import User, UserAchievement
from app.schemas.achievement_schemas import AchievementCreate


def create_achievement(
        db: Session,
        achievement: AchievementCreate
):
    """
    Создание нового достижения в базе данных.
    :param db: Сессия базы данных.
    :param achievement: Данные о достижении.
    :return: Возвращает созданное достижение.
    """
    db_achievement = Achievement(**achievement.model_dump())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement


def get_achievements(db: Session):
    return db.query(Achievement).all()


def users_with_max_achievements(db: Session):
    """
    Находит пользователей с максимальным количеством достижений.
    :param db: Сессия базы данных.
    :return: Список словарей с информацией о пользователях.
    """
    # Шаг 1: Получаем максимальное количество достижений
    max_achievements = (
        db.query(func.count(UserAchievement.id))
        .select_from(UserAchievement)
        .join(User, User.id == UserAchievement.user_id)
        .group_by(UserAchievement.user_id)
        .order_by(func.count(UserAchievement.id).desc())
        .limit(1)
        .scalar()
    )

    # Шаг 2: Получаем пользователей с максимальным количеством достижений
    max_users = (
        db.query(
            User.id.label("user_id"),
            User.name.label("user_name"),
            func.count(UserAchievement.id).label("achievement_count")
        )
        .join(UserAchievement, User.id == UserAchievement.user_id)
        .group_by(User.id)
        .having(func.count(UserAchievement.id) == max_achievements)
        .all()
    )

    return [
        {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "achievement_count": user.achievement_count,
        }
        for user in max_users
    ]


def user_with_max_points(db: Session):
    """
    Находит пользователей с максимальным количеством очков достижений.
    :param db: Сессия базы данных.
    :return: Список пользователей с максимальным количеством очков.
    """
    # Подзапрос для вычисления сумм очков для каждого пользователя
    subquery = (
        db.query(
            User.id.label("user_id"),
            User.name.label("user_name"),
            func.sum(Achievement.points).label("total_points")
        )
        .join(UserAchievement, User.id == UserAchievement.user_id)
        .join(Achievement, UserAchievement.achievement_id == Achievement.id)
        .group_by(User.id)
        .subquery()
    )

    # Подзапрос для нахождения максимальной суммы очков
    max_points = (
        db.query(func.max(subquery.c.total_points))
        .scalar()
    )

    # Запрос для получения пользователей с максимальной суммой очков
    result = (
        db.query(
            subquery.c.user_id,
            subquery.c.user_name,
            subquery.c.total_points,
        )
        .filter(subquery.c.total_points == max_points)
        .all()
    )

    users = [
        {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "total_points": user.total_points,
        }
        for user in result
    ]

    return users


def get_users_with_points_difference(
        db: Session,
        find_max: bool = True
):
    """
    Универсальная функция для поиска пользователей с максимальной или минимальной разницей очков достижений.
    :param db: Сессия базы данных.
    :param find_max: Если флаг равен True - ищет максимальную разницу, иначе минимальную.
    :return: Список пар пользователей с соответствующей разностью очков.
    """
    # Подзапрос для получения суммарных очков пользователей
    user_points = (
        db.query(
            User.id.label("user_id"),
            User.name.label("user_name"),
            func.sum(Achievement.points).label("total_points")
        )
        .join(UserAchievement, User.id == UserAchievement.user_id)
        .join(Achievement, UserAchievement.achievement_id == Achievement.id)
        .group_by(User.id)
        .subquery()
    )

    # Создание алиасов для самосоединения
    user1 = aliased(user_points)
    user2 = aliased(user_points)

    # Запрос для получения пар пользователей и разности очков
    paired_users = (
        db.query(
            user1.c.user_id.label("user_1_id"),
            user1.c.user_name.label("user_1_name"),
            user1.c.total_points.label("user_1_points"),
            user2.c.user_id.label("user_2_id"),
            user2.c.user_name.label("user_2_name"),
            user2.c.total_points.label("user_2_points"),
            func.abs(user1.c.total_points - user2.c.total_points).label("points_difference"),
        )
        .filter(user1.c.user_id < user2.c.user_id)  # Исключаем повторяющиеся пары
        .subquery()
    )

    # Определяем, искать максимальную или минимальную разницу
    points_difference = (
        db.query(func.max(paired_users.c.points_difference)).scalar()
        if find_max
        else db.query(func.min(paired_users.c.points_difference)).scalar()
    )

    if points_difference is None:
        raise HTTPException(status_code=404, detail="Not enough data to calculate differences")

    # Получение всех пар с соответствующей разностью
    result = (
        db.query(paired_users)
        .filter(paired_users.c.points_difference == points_difference)
        .all()
    )

    return [
        {
            "user_1": {
                "id": pair.user_1_id,
                "name": pair.user_1_name,
                "total_points": pair.user_1_points,
            },
            "user_2": {
                "id": pair.user_2_id,
                "name": pair.user_2_name,
                "total_points": pair.user_2_points,
            },
            "points_difference": pair.points_difference,
        }
        for pair in result
    ]


def users_with_7_day_streak(db: Session):
    """
    Находит пользователей, которые получали достижения 7 дней подряд.
    :param db: Сессия базы данных.
    :return: Список пользователей с информацией о 7-дневной серии.
    """
    # Оконная функция для ROW_NUMBER
    streak_row_number = over(
        func.row_number(),
        partition_by=UserAchievement.user_id,
        order_by=func.date(UserAchievement.issued_at)
    )

    # Группирующий идентификатор последовательности
    streak_group = func.date_part(
        'epoch',
        func.date(UserAchievement.issued_at)
    ) // (24 * 60 * 60) - streak_row_number.cast(Integer)

    # Подзапрос для вычисления streak_group
    subquery = (
        db.query(
            UserAchievement.user_id,
            func.date(UserAchievement.issued_at).label("achievement_date"),
            streak_group.label("streak_group")
        )
        .subquery()
    )

    # Запрос для нахождения групп с минимум 7 днями подряд
    streak_query = (
        db.query(subquery.c.user_id)
        .group_by(subquery.c.user_id, subquery.c.streak_group)
        .having(func.count().label("streak_length") >= 6)
    )

    # Выполнение запроса и получение результатов
    result = streak_query.all()

    # Возвращаем id пользователей
    return set(row.user_id for row in result)
