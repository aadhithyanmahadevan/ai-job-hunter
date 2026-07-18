from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import hash_password, verify_password
from app.database.session import get_db
from app.database.user_repository import UserRepository
from app.database.refresh_token_repository import RefreshTokenRepository

from app.models.user import User

from app.schemas.auth import (
    TokenResponse,
    RefreshTokenRequest,
)

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    is_refresh_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)

    if repo.get_by_email(user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    logger.info(f"User registered: {user.email}")

    return repo.create(new_user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)

    user = repo.get_by_email(form_data.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        {
            "sub": user.email,
            "user_id": user.id,
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": user.email,
            "user_id": user.id,
        }
    )

    refresh_repo = RefreshTokenRepository(db)

    refresh_repo.create(
        token=refresh_token,
        user_id=user.id,
    )

    logger.info(f"User logged in: {user.email}")

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    refresh_repo = RefreshTokenRepository(db)

    stored_token = refresh_repo.get(
        request.refresh_token,
    )

    if stored_token is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found",
        )

    if stored_token.revoked:
        raise HTTPException(
            status_code=401,
            detail="Refresh token revoked",
        )

    payload = decode_access_token(
        request.refresh_token,
    )

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if not is_refresh_token(payload):
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    refresh_repo.revoke(
        request.refresh_token,
    )

    access_token = create_access_token(
        {
            "sub": payload["sub"],
            "user_id": payload["user_id"],
        }
    )

    new_refresh_token = create_refresh_token(
        {
            "sub": payload["sub"],
            "user_id": payload["user_id"],
        }
    )

    refresh_repo.create(
        token=new_refresh_token,
        user_id=payload["user_id"],
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


@router.post("/logout")
def logout(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    repo = RefreshTokenRepository(db)

    repo.revoke(
        request.refresh_token,
    )

    return {
        "message": "Logged out successfully."
    }