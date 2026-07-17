import hashlib
import json
from pathlib import Path


CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)


class ResumeCache:

    @staticmethod
    def get_hash(text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def cache_path(hash_value: str) -> Path:
        return CACHE_DIR / f"{hash_value}.json"

    @classmethod
    def exists(cls, hash_value: str) -> bool:
        return cls.cache_path(hash_value).exists()

    @classmethod
    def load(cls, hash_value: str):

        with open(
            cls.cache_path(hash_value),
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    @classmethod
    def save(
        cls,
        hash_value: str,
        data: dict,
    ):

        with open(
            cls.cache_path(hash_value),
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
            )