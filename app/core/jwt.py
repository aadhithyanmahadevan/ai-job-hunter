from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.config.settings import settings


def _create_token(
    data: dict[str, Any],
    expires_delta: timedelta,
    token_type: str,
) -> str:
    payload = data.copy()

    payload.update(
        {
            "exp": datetime.now(timezone.utc) + expires_delta,
            "type": token_type,
        }
    )

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(data: dict[str, Any]) -> str:
    return _create_token(
        data=data,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
        token_type="access",
    )


def create_refresh_token(data: dict[str, Any]) -> str:
    return _create_token(
        data=data,
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        ),
        token_type="refresh",
    )


def decode_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError:
        return None

def is_refresh_token(payload: dict) -> bool:
    return payload.get("type") == "refresh"


def is_access_token(payload: dict) -> bool:
    return payload.get("type") == "access"

# Backward compatibility
def decode_access_token(token: str):
    return decode_token(token)