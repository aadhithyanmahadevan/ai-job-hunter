import json

from sqlalchemy.orm import Session

from app.database.job_repository import JobRepository
from app.database.match_repository import MatchRepository
from app.database.resume_repository import ResumeRepository
from app.models.match import Match
from app.providers.gemini_provider import GeminiProvider


class MatchService:

    def __init__(self, db: Session):
        self.db = db
        self.resume_repo = ResumeRepository(db)
        self.job_repo = JobRepository(db)
        self.match_repo = MatchRepository(db)
        self.ai = GeminiProvider()

    def analyze(
        self,
        resume_text: str,
        job_description: str,
    ):
        result = self.ai.match_resume_to_job(
            resume_text,
            job_description,
        )

        if isinstance(result, str):
            result = json.loads(result)

        return result

    def match_resume(self, resume_id: int):

        resume = self.resume_repo.get(resume_id)

        if not resume:
            raise Exception("Resume not found.")

        jobs = self.job_repo.get_all()

        if not jobs:
            raise Exception("No jobs found.")

        # Remove old matches
        self.match_repo.delete_by_resume(resume_id)

        matches = []

        for job in jobs:

            result = self.analyze(
                resume.extracted_text,
                job.description,
            )

            match = Match(
                resume_id=resume.id,
                job_id=job.id,
                match_score=result.get("score", 0),
                matched_skills=json.dumps(
                    result.get("strengths", [])
                ),
                missing_skills=json.dumps(
                    result.get("missing_skills", [])
                ),
                recommendations=result.get(
                    "recommendation",
                    "",
                ),
                raw_json=json.dumps(result),
            )

            self.match_repo.create(match)

            matches.append(
                {
                    "job_id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "salary": job.salary,
                    "match_score": result.get("score", 0),
                    "matched_skills": result.get(
                        "strengths",
                        [],
                    ),
                    "missing_skills": result.get(
                        "missing_skills",
                        [],
                    ),
                    "recommendation": result.get(
                        "recommendation",
                        "",
                    ),
                }
            )

        matches.sort(
            key=lambda x: x["match_score"],
            reverse=True,
        )

        return {
            "resume_id": resume.id,
            "total_jobs": len(jobs),
            "matched_jobs": len(matches),
            "top_matches": matches,
        }