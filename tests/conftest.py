import os
from pathlib import Path
from dotenv import load_dotenv

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import app


client = TestClient(app)

current_path = Path.cwd()
env_path = Path(current_path, '.env')

load_dotenv()


class TestSettings(BaseModel):
    # Настройки тестовой базы данных
    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD')
    postgres_host_test: str = os.getenv('POSTGRES_HOST_TEST')
    postgres_port_test: int = os.getenv("POSTGRES_PORT_TEST")
    postgres_db_test: str = os.getenv("POSTGRES_DB_TEST")

    api_v1_prefix: str = "api/v1"

    # Генерация PostgresDsn
    @property
    def database_test_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host_test}:{self.postgres_port_test}/"
            f"{self.postgres_db_test}"
        )

# Экземпляр настроек для использования в приложении
settings = TestSettings()


@pytest.fixture(scope="function", autouse=True)
def override_settings(monkeypatch):
    # Установим переменную окружения для тестовой базы данных
    monkeypatch.setenv(
        "POSTGRES_HOST",
        settings.postgres_host_test,
    )
    monkeypatch.setenv(
        "POSTGRES_PORT",
        str(settings.postgres_port_test),
    )
    monkeypatch.setenv(
        "POSTGRES_DB",
        settings.postgres_db_test,
    )
    print(f"POSTGRES_DB used: {os.getenv('POSTGRES_DB')}")

    yield
