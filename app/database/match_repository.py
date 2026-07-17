from sqlalchemy.orm import Session

from app.models.match import Match


class MatchRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, match: Match):
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        return match

    def get(self, match_id: int):
        return self.db.query(Match).filter(Match.id == match_id).first()

    def get_by_resume(self, resume_id: int):
        return (
            self.db.query(Match)
            .filter(Match.resume_id == resume_id)
            .order_by(Match.match_score.desc())
            .all()
        )

    def delete(self, match: Match):
        self.db.delete(match)
        self.db.commit()

    def delete_by_resume(self, resume_id: int):
        (self.db.query(Match).filter(Match.resume_id == resume_id).delete())
        self.db.commit()

    def count(self):
        return self.db.query(Match).count()
