from datetime import datetime

from pydantic import BaseModel


class AchievementBase(BaseModel):
    name_en: str
    name_ru: str
    points: int
    description_en: str
    description_ru: str


class AchievementCreate(AchievementBase):
    pass


class Achievement(AchievementBase):
    id: int

    class Config:
        from_attributes = True


class AchievementOut(BaseModel):
    id: int
    name: str
    description: str
    points: int
    issued_at: datetime


class UserAchievementsOut(BaseModel):
    user_id: int
    achievements: list[AchievementOut] = []

    class Config:
        from_attributes = True
