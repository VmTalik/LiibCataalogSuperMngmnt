import os
from typing import Tuple
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


class EngineConfig(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 5


class DBConfig(BaseModel):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int


class TestDBConfig(DBConfig):
    pass


def get_env_file_paths(*file_names: str) -> Tuple[str, ...]:
    directory = os.path.dirname(os.path.abspath(__file__))
    env_file_paths = tuple(os.path.join(directory, "../../", file_name) for file_name in file_names)
    return env_file_paths


class Settings(BaseSettings):
    db_config: DBConfig
    test_db_config: TestDBConfig
    engine_config: EngineConfig = EngineConfig()
    run_config: RunConfig = RunConfig()
    model_config = SettingsConfigDict(
        env_file=get_env_file_paths(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__"
    )


settings = Settings()


def get_db_url(test_db: bool = False) -> str:
    config: DBConfig = settings.db_config
    if test_db:
        config: TestDBConfig = settings.test_db_config

    return (f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@"
            f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
