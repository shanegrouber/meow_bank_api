from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base settings
    ENVIRONMENT: str = "development"

    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database settings
    DATABASE_URL: str = "sqlite:///./meow_bank.db"

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
