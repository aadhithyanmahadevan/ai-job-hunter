import json
from collections import Counter

from app.database.analysis_repository import AnalysisRepository
from app.database.match_repository import MatchRepository
from app.database.resume_repository import ResumeRepository


class DashboardService:

    def __init__(self, db):
        self.resume_repo = ResumeRepository(db)
        self.analysis_repo = AnalysisRepository(db)
        self.match_repo = MatchRepository(db)

    def get_dashboard(self, resume_id: int):

        analysis = self.analysis_repo.get_by_resume(resume_id)
        matches = self.match_repo.get_by_resume(resume_id)

        if not matches:

            return {
                "resume_score": analysis.ats_score if analysis else 0,
                "jobs_analyzed": 0,
                "average_match": 0,
                "highest_match": 0,
                "lowest_match": 0,
                "top_missing_skills": [],
            }

        scores = [m.match_score for m in matches]

        counter = Counter()

        for match in matches:

            try:
                skills = json.loads(match.missing_skills)
                counter.update(skills)
            except Exception:
                pass

        return {
            "resume_score": analysis.ats_score if analysis else 0,
            "jobs_analyzed": len(matches),
            "average_match": round(sum(scores) / len(scores), 2),
            "highest_match": max(scores),
            "lowest_match": min(scores),
            "top_missing_skills": [
                skill for skill, _ in counter.most_common(10)
            ],
        }