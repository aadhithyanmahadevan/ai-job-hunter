import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Settings:

    APP_NAME = "AI Job Hunter"
    APP_VERSION = "1.0.0"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = "models/gemini-3.5-flash"

    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///data/jobs.db"
    )


settings = Settings()