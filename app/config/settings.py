import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME: str = "AI Job Hunter"
    APP_VERSION: str = "1.0.0"

    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = "models/gemini-3.5-flash"

    ADZUNA_APP_ID: str | None = os.getenv("ADZUNA_APP_ID")
    ADZUNA_APP_KEY: str | None = os.getenv("ADZUNA_APP_KEY")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///data/jobs.db",
    )

    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "change-this-in-production",
    )

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
    )


settings = Settings()