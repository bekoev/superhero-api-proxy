from __future__ import annotations

import sys
from logging.config import dictConfig

from app.plugins.logger.settings import LoggerSettings
from app.settings import AppSettings


class LoggingConfiguration:
    """The class to handle logging configuration for the whole application."""

    def __init__(
        self, app_settings: AppSettings, logger_settings: LoggerSettings
    ) -> None:
        self.logger_level = logger_settings.level
        self.logger_name = app_settings.name.replace("-", "_")

    def apply_configuration(self) -> None:
        dictConfig(self.get_config_dict())

    def get_config_dict(self) -> dict:
        logging_lvl = self.logger_level

        config = {
            "version": 1,
            "disable_existing_loggers": True,
            #
            "loggers": {
                self.logger_name: {
                    "level": logging_lvl,
                    "propagate": False,
                    "handlers": ["console_plain"],
                },
                "uvicorn": {
                    "level": logging_lvl,
                    "propagate": False,
                    "handlers": ["console_plain"],
                },
                "uvicorn.access": {
                    "level": logging_lvl,
                    "propagate": False,
                    "handlers": ["console_plain"],
                },
                "uvicorn.errors": {
                    "level": logging_lvl,
                    "propagate": False,
                    "handlers": ["console_plain"],
                },
            },
            #
            "handlers": {
                "console_plain": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "plain",
                },
            },
            #
            "formatters": {
                "plain": {
                    "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
        }

        return config
