from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings


# Создаем движок для базы данных
engine = create_engine(settings.database_url, echo=True)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Генератор сессий баз данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Тип SessionDep
# Указывает, что при использовании SessionDep
# FastAPI должно вызвать функцию get_db через
# Depends для получения объекта типа Session.
SessionDep = Annotated[Session, Depends(get_db)]
