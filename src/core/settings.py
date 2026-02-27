from typing import ClassVar, List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    PROJECT_NAME: str = "Local"
    PROJECT_DESCRIPTION: str = "Hello worlds!\nIt's project Local"

    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent
    MEDIA_DIR: ClassVar[Path] = BASE_DIR / "media"
    STATIC_DIR: ClassVar[Path] = BASE_DIR / "static"
    TEMPLATE_DIR: ClassVar[Path] = BASE_DIR / "templates"
    CORS_ORIGINS: List[str] = ["*"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_USE_TLS: bool
    EMAIL_USE_SSL: bool

    TOKEN: str
    REDIS_URL: str
    REDIS_HOST: str
    REDIS_PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    @property
    def DATA_BASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATA_BASE_URL_sync(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def media_path(self) -> Path:
        return self.MEDIA_DIR

    @property
    def static_path(self) -> Path:
        return self.STATIC_DIR

    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()
