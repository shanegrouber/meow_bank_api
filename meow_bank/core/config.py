from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./meow_bank.db"

    MEOW_BANK_API_KEY: str = "test_api_key"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields in env vars
    )

    @property
    def DEBUG(self) -> bool:  # noqa: N802
        return self.ENVIRONMENT == "development"

    @property
    def LOG_LEVEL(self) -> str:  # noqa: N802
        return "DEBUG" if self.DEBUG else "INFO"


settings = Settings()
