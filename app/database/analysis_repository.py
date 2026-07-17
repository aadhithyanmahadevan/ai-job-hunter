from sqlalchemy.orm import Session

from app.models.resume_analysis import ResumeAnalysis


class AnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        analysis: ResumeAnalysis,
    ):
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def get(self, analysis_id: int):
        return (
            self.db.query(ResumeAnalysis)
            .filter(ResumeAnalysis.id == analysis_id)
            .first()
        )

    def get_by_resume(
        self,
        resume_id: int,
    ):
        return (
            self.db.query(ResumeAnalysis)
            .filter(ResumeAnalysis.resume_id == resume_id)
            .order_by(ResumeAnalysis.created_at.desc())
            .first()
        )

    def get_all_by_resume(
        self,
        resume_id: int,
    ):
        return (
            self.db.query(ResumeAnalysis)
            .filter(ResumeAnalysis.resume_id == resume_id)
            .order_by(ResumeAnalysis.created_at.desc())
            .all()
        )

    def delete(
        self,
        analysis: ResumeAnalysis,
    ):
        self.db.delete(analysis)
        self.db.commit()

    def count(self):
        return self.db.query(ResumeAnalysis).count()
