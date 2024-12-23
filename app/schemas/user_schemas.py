from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.enums.languages import LanguageEnum


class UserBase(BaseModel):
    name: str = Field(min_length=2)
    language: Optional[LanguageEnum] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserAchievementBase(BaseModel):
    user_id: int
    achievement_id: int


class UserAchievementCreate(BaseModel):
    achievement_id: int


class UserAchievement(UserAchievementBase):
    id: int
    issued_at: datetime

    class Config:
        from_attributes = True
