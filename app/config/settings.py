import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME = "AI Job Hunter"
    APP_VERSION = "1.0.0"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY", "")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/jobs.db")


settings = Settings()