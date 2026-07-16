from app.models.match import JobMatch
from app.services.similarity import calculate_skill_match


class MatchingAgent:

    def match_jobs(
        self,
        resume: dict,
        jobs: list,
    ):

        results = []

        resume_skills = resume.get("skills", [])

        for job in jobs:

            job_skills = job.get("skills", [])

            score, matched, missing = calculate_skill_match(
                resume_skills,
                job_skills,
            )

            results.append(
                JobMatch(
                    title=job["title"],
                    company=job["company"],
                    location=job["location"],
                    url=job["url"],
                    match_score=score,
                    matched_skills=matched,
                    missing_skills=missing,
                )
            )

        return sorted(
            results,
            key=lambda x: x.match_score,
            reverse=True,
        )