from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        token: str,
        user_id: int,
    ) -> RefreshToken:

        refresh = RefreshToken(
            token=token,
            user_id=user_id,
        )

        self.db.add(refresh)
        self.db.commit()
        self.db.refresh(refresh)

        return refresh

    def get(
        self,
        token: str,
    ) -> RefreshToken | None:

        return (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token == token)
            .first()
        )

    def revoke(
        self,
        token: str,
    ) -> None:

        refresh = self.get(token)

        if refresh:
            refresh.revoked = True
            self.db.commit()