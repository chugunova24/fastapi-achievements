from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app.db.base import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name_en: Mapped[str] = mapped_column(String, nullable=False)
    name_ru: Mapped[str] = mapped_column(String, nullable=False)
    description_en: Mapped[str] = mapped_column(String, nullable=False)
    description_ru: Mapped[str] = mapped_column(String, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
