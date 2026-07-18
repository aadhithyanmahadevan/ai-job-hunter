from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User


class AuthService:
    @staticmethod
    def register(
        db: Session,
        full_name: str,
        email: str,
        password: str,
    ) -> User:

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            raise ValueError("Email already registered.")

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ):

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password.")

        access = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        refresh = create_refresh_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer",
        }