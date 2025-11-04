from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """General settings for the application"""

    name: str = "superhero-api-proxy"
    host: str = "localhost"
    port: int = 8080

    superhero_api_base_url: str = "https://superheroapi.com/api.php/"
    superhero_api_access_token: str = ""

    model_config = SettingsConfigDict(
        env_prefix="app_",
        env_file=".env",
        frozen=True,
        extra="ignore",
    )
