from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "IPO Insight Platform"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./ipo.db"
    SECRET_KEY: str = "change-this-to-a-strong-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALPHAVANTAGE_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()