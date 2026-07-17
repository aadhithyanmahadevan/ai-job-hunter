from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        resume: Resume,
    ):
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def update(
        self,
        resume: Resume,
    ):
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get(
        self,
        resume_id: int,
    ):
        return self.db.query(Resume).filter(Resume.id == resume_id).first()

    def get_by_user(
        self,
        user_id: int,
    ):
        return (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.uploaded_at.desc())
            .all()
        )

    def delete(
        self,
        resume: Resume,
    ):
        self.db.delete(resume)
        self.db.commit()

    def count(self):
        return self.db.query(Resume).count()
