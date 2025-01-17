from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


current_path = Path.cwd()
env_path = Path(current_path, '.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Основные настройки приложения
    app_host: str = Field(alias="APP_HOST")
    app_port: int = Field(alias="APP_PORT")

    # Настройки базы данных
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")

    # Генерация PostgresDsn
    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # Настройки Nginx
    nginx_port: int = Field(alias="NGINX_PORT")

    # Дополнительные настройки
    environment: str = Field(default="development", alias="ENV")


# Экземпляр настроек для использования в приложении
settings = Settings()
