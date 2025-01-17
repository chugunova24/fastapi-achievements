from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette import status

from app.models.achievement import Achievement
from app.models.user import User
from app.schemas.user_schemas import UserCreate
from app.schemas.user_schemas import UserAchievementCreate
from app.models.user import UserAchievement


def create_user(
        db: Session,
        user: UserCreate
):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(User).all()


def issue_achievement(
        user_id,
        db: Session,
        user_achievement: UserAchievementCreate
):
    # Проверяем, существует ли пользователь
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Проверяем, не было ли уже выдано это достижение пользователю
    existing_achievement = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == user_achievement.achievement_id
    ).first()

    if existing_achievement:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Achievement already awarded"
        )

    # Создание нового достижения для пользователя
    db_user_achievement = UserAchievement(
        **user_achievement.model_dump(),
        user_id=user_id
    )
    db.add(db_user_achievement)
    db.commit()
    db.refresh(db_user_achievement)

    # Получаем все достижения пользователя с их локализованными данными
    user_achievements = (
        db.query(UserAchievement)
        .join(Achievement)
        .filter(UserAchievement.user_id == user_id)
        # Оптимизация запроса для подгрузки достижений
        .options(joinedload(UserAchievement.achievement))
        .all()
    )

    achievements = []
    for ua in user_achievements:
        achievement = ua.achievement
        achievements.append({
            "id": achievement.id,
            "name": getattr(achievement,
                            f"name_{user.language}",
                            achievement.name_en),  # Локализация имени
            "points": achievement.points,
            "description": getattr(
                achievement,
                f"description_{user.language}",
                achievement.description_en),  # Локализация описания
            "issued_at": ua.issued_at
        })

    return {"user_id": user_id, "achievements": achievements}


def get_user_achievements(
        user_id: int,
        db: Session
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_achievements = (
        db.query(
            UserAchievement.id,
            Achievement.id.label("achievement_id"),
            Achievement.name_en,
            Achievement.name_ru,
            Achievement.points,
            Achievement.description_en,
            Achievement.description_ru,
            UserAchievement.issued_at
        )
        .join(Achievement, UserAchievement.achievement_id == Achievement.id)
        .filter(UserAchievement.user_id == user_id)
        .all()
    )

    achievements = [
        {
            "id": row.achievement_id,
            "name": getattr(row, f"name_{user.language}", row.name_en),
            "description":  getattr(row,
                                    f"description_{user.language}",
                                    row.description_en),
            "points":  row.points,
            "issued_at": row.issued_at,
        }
        for row in user_achievements
    ]

    return {
        "user_id": user.id,
        "achievements": achievements
    }
