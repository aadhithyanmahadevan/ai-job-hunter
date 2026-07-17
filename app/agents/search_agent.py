from sqlalchemy.orm import Session

from app.database.models import Job
from app.database.repository import JobRepository
from app.providers.gemini_provider import GeminiProvider
from app.services.adzuna import AdzunaProvider
from app.services.normalizer import normalize_adzuna
from app.services.state import state
from app.services.job_cache import JobSkillCache


class JobSearchAgent:

    def __init__(self, db: Session):

        self.provider = AdzunaProvider()
        self.repo = JobRepository(db)

        # Gemini AI
        self.ai = GeminiProvider()

    def search(self):

        response = self.provider.search_jobs()

        jobs = []

        added = 0

        for item in response["results"]:

            normalized = normalize_adzuna(item)

            # ------------------------------------------
            # AI Skill Extraction
            # ------------------------------------------

            try:

                job_hash = JobSkillCache.get_hash(
                    normalized.description
                )   

                if JobSkillCache.exists(job_hash):

                    print("Loaded skills from cache")

                    extracted = JobSkillCache.load(job_hash)

                else:

                    print("Extracting skills using Gemini")

                    extracted = self.ai.extract_job_skills(
                        normalized.description
                    )

                    JobSkillCache.save(
                        job_hash,
                        extracted
                    )

                skills = extracted.get("skills", [])
                
            except Exception as e:

                print("Skill extraction failed:", e)

                skills = []

            # ------------------------------------------

            jobs.append(
                {
                    "title": normalized.title,
                    "company": normalized.company,
                    "location": normalized.location,
                    "description": normalized.description,
                    "salary": f"{normalized.salary_min}-{normalized.salary_max}",
                    "url": normalized.url,
                    "source": normalized.source,
                    "skills": skills,
                }
            )

            if not self.repo.exists(normalized.url):

                job = Job(
                    title=normalized.title,
                    company=normalized.company,
                    location=normalized.location,
                    description=normalized.description,
                    salary=f"{normalized.salary_min}-{normalized.salary_max}",
                    url=normalized.url,
                    source=normalized.source,
                )

                self.repo.save(job)

                added += 1

        state.jobs = jobs

        return {
            "new_jobs_added": added,
            "total_jobs": self.repo.count(),
            "jobs": jobs,
        }