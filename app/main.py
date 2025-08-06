import uvicorn

from app.api.server import create_app
from app.core.containers import container

app = create_app(container)


def main() -> None:
    config = container.config()
    container.logger().info(f"-- Start {config.app.name}")
    uvicorn.run(
        "app.main:app",
        host=config.app.host,
        port=config.app.port,
        log_config=container.logging_config().get_config_dict(),
    )
