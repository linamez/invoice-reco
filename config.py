from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Load configuration from environment variables or a .env file
    """

    openai_api_key: str | None = None
    model_config = SettingsConfigDict(env_file=".env")


config = Config()
