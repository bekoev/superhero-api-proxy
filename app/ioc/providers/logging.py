import logging

from dishka import Provider, Scope, provide

from app.plugins.logger.logging_config import LoggingConfiguration


class LoggingProvider(Provider):
    logging_config = provide(LoggingConfiguration, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def logger(self, config: LoggingConfiguration) -> logging.Logger:
        config.apply_configuration()
        return logging.getLogger(config.logger_name)
