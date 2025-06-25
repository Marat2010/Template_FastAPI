from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Dict


class RunConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000


class LogConfig(BaseModel):
    LOGGER_NAME: str = "templ_fa"
    # LOG_LEVEL: str = "INFO"
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str | None = "logs/app.log"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    book: str = "/book"
    # new_entity: str = "/new_entity"


class ApiPrefix(BaseModel):
    prefix: str = '/api'
    v1: ApiV1Prefix = ApiV1Prefix()
    version: str = "1.01"
    title: str = f"API project: {LogConfig().LOGGER_NAME.capitalize()}"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: Dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    log: LogConfig = LogConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
