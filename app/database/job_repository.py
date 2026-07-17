from sqlalchemy.orm import Session

from app.models.job import Job


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def exists(self, url: str):
        return (
            self.db.query(Job)
            .filter(Job.url == url)
            .first()
            is not None
        )

    def save(self, job: Job):
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_all(self):
        return self.db.query(Job).all()

    def count(self):
        return self.db.query(Job).count()