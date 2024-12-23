import os
from pathlib import Path
from dotenv import load_dotenv

from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import app


client = TestClient(app)

current_path = Path.cwd()
env_path = Path(current_path, '.env')

load_dotenv()


class Settings(BaseModel):
    # Настройки тестовой базы данных
    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD')
    postgres_host: str = os.getenv('POSTGRES_HOST_TEST')
    postgres_port: int = os.getenv("POSTGRES_PORT_TEST")
    postgres_db_test: str = os.getenv("POSTGRES_DB_TEST")


    api_v1_prefix: str = "api/v1"

    # Генерация PostgresDsn
    @property
    def database_test_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db_test}"
        )


# Экземпляр настроек для использования в приложении
settings = Settings()

# engine = create_engine(settings.database_test_url)
# SessionTest = sessionmaker(bind=engine)
#
#
# def get_test_db():
#     db = SessionTest()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @pytest.fixture(scope="function")
# def db_test_session():
#     """
#     Фикстура для создания и уничтожения тестовой базы данных
#     """
#     # Создаем тестовую базу данных
#     Base.metadata.create_all(bind=engine)
#
#     # Создаем сессию для работы с базой данных
#     SessionTest.configure(bind=engine)
#     db = SessionTest()
#
#     yield db
#
#     # Очистка базы данных после каждого теста
#     db.close()
#     Base.metadata.drop_all(bind=engine)
