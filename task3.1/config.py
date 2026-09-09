# config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    LLM_MODEL: str
    LLM_TEMPERATURE: float
    LLM_TIMEOUT: float
    LLM_MAX_RETRIES: int
    LLM_CACHE_TTL: int
    APP_NAME: str
    APP_VERSION: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()