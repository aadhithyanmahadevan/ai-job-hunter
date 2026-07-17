from sqlalchemy.orm import Session

from app.models.job import Job
from app.database.job_repository import JobRepository
from app.providers.gemini_provider import GeminiProvider
from app.services.adzuna import AdzunaProvider
from app.services.normalizer import normalize_adzuna
from app.services.job_cache import JobSkillCache


class JobSearchAgent:

    def __init__(self, db: Session):
        self.provider = AdzunaProvider()
        self.repo = JobRepository(db)
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

                job_hash = JobSkillCache.get_hash(normalized.description)

                if JobSkillCache.exists(job_hash):

                    print("Loaded skills from cache")

                    extracted = JobSkillCache.load(job_hash)

                else:

                    print("Extracting skills using Gemini")

                    extracted = self.ai.extract_job_skills(normalized.description)

                    JobSkillCache.save(job_hash, extracted)

                skills = extracted.get("skills", [])

            except Exception as e:

                print("Skill extraction failed:", e)

                skills = []

            # ------------------------------------------
            # Salary Formatting
            # ------------------------------------------

            if normalized.salary_min is not None and normalized.salary_max is not None:
                salary = (
                    f"₹{normalized.salary_min:,.0f} - " f"₹{normalized.salary_max:,.0f}"
                )

            elif normalized.salary_min is not None:
                salary = f"From ₹{normalized.salary_min:,.0f}"

            elif normalized.salary_max is not None:
                salary = f"Up to ₹{normalized.salary_max:,.0f}"

            else:
                salary = "Not disclosed"

            # ------------------------------------------
            # Response Object
            # ------------------------------------------

            jobs.append(
                {
                    "title": normalized.title,
                    "company": normalized.company,
                    "location": normalized.location,
                    "description": normalized.description,
                    "salary": salary,
                    "url": normalized.url,
                    "source": normalized.source,
                    "skills": skills,
                }
            )

            # ------------------------------------------
            # Save to Database
            # ------------------------------------------

            if not self.repo.exists(normalized.url):

                job = Job(
                    title=normalized.title,
                    company=normalized.company,
                    location=normalized.location,
                    description=normalized.description,
                    salary=salary,
                    url=normalized.url,
                    source=normalized.source,
                )

                self.repo.save(job)

                added += 1

        return {
            "new_jobs_added": added,
            "total_jobs": self.repo.count(),
            "jobs": jobs,
        }
