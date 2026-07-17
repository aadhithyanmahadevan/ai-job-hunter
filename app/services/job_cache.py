import hashlib
import json
from pathlib import Path

CACHE_DIR = Path("cache/jobs")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class JobSkillCache:

    @staticmethod
    def get_hash(description: str) -> str:
        return hashlib.sha256(
            description.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def get_file(hash_value: str) -> Path:
        return CACHE_DIR / f"{hash_value}.json"

    @classmethod
    def exists(cls, hash_value: str) -> bool:
        return cls.get_file(hash_value).exists()

    @classmethod
    def load(cls, hash_value: str):

        with open(
            cls.get_file(hash_value),
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    @classmethod
    def save(
        cls,
        hash_value: str,
        data: dict
    ):

        with open(
            cls.get_file(hash_value),
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )