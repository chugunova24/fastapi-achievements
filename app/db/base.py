from sqlalchemy.orm import declarative_base

# Базовый класс для моделей баз данных
Base = declarative_base()


from app.models.achievement import *
from app.models.user import *
