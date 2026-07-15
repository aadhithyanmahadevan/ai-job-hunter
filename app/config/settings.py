from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Job Hunter"
    APP_VERSION: str = "1.0.0"

    OPENAI_API_KEY: str = ""
    JSEARCH_API_KEY: str = ""

    DATABASE_URL: str = "sqlite:///data/jobs.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()