from __future__ import annotations

import logging
import sys
from logging.config import dictConfig

from app.settings import MainSettings


def init_logging(config: LoggingConfiguration) -> logging.Logger:
    config.apply_configuration()
    return logging.getLogger(config.logger_name)


class LoggingConfiguration:
    """The class to handle logging configuration for the whole application."""

    def __init__(self, app_settings: MainSettings) -> None:
        self._app_settings = app_settings
        self.logger_name = self._app_settings.app.name.replace("-", "_")

    def apply_configuration(self) -> None:
        dictConfig(self.get_config_dict())

    def get_config_dict(self) -> dict:
        logging_lvl = self._app_settings.logger.level

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
