from sqlalchemy.orm import Session

from app.database.models import Job
from app.database.repository import JobRepository
from app.services.adzuna import AdzunaProvider
from app.services.normalizer import normalize_adzuna
from app.services.state import state


class JobSearchAgent:

    def __init__(self, db: Session):

        self.provider = AdzunaProvider()
        self.repo = JobRepository(db)

    def search(self):

        response = self.provider.search_jobs()

        jobs = []

        added = 0

        for item in response["results"]:

            normalized = normalize_adzuna(item)

            jobs.append(
                {
                    "title": normalized.title,
                    "company": normalized.company,
                    "location": normalized.location,
                    "description": normalized.description,
                    "salary": f"{normalized.salary_min}-{normalized.salary_max}",
                    "url": normalized.url,
                    "source": normalized.source,
                    "skills": [],
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