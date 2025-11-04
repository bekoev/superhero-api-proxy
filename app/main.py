import uvicorn

from app.api.server import create_production_app
from app.plugins.logger.logging_config import LoggingConfiguration
from app.plugins.logger.settings import LoggerSettings
from app.settings import AppSettings

app = create_production_app()


def main() -> None:
    app_settings = AppSettings()
    logging_config = LoggingConfiguration(AppSettings(), LoggerSettings())
    uvicorn.run(
        "app.main:app",
        host=app_settings.host,
        port=app_settings.port,
        log_config=logging_config.get_config_dict(),
    )
