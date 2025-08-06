from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingLVL(StrEnum):
    INFO = "INFO"
    DEBUG = "DEBUG"


class LoggerSettings(BaseSettings):
    level: LoggingLVL = LoggingLVL.INFO

    model_config = SettingsConfigDict(
        env_prefix="logger_",
        env_file=".env",
        frozen=True,
        extra="ignore",
    )


@lru_cache
def get_config():
    return LoggerSettings()
