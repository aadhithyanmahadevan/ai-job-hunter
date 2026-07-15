from sqlalchemy.orm import Session

from app.database.models import Job
from app.database.repository import JobRepository
from app.services.adzuna import AdzunaProvider
from app.services.normalizer import normalize_adzuna


class JobSearchAgent:

    def __init__(self, db: Session):
        self.provider = AdzunaProvider()
        self.repo = JobRepository(db)

    def search(self):

        response = self.provider.search_jobs()

        added = 0

        for item in response["results"]:

            normalized = normalize_adzuna(item)

            if self.repo.exists(normalized.url):
                continue

            job = Job(
                title=normalized.title,
                company=normalized.company,
                location=normalized.location,
                description=normalized.description,
                salary=str(
                    f"{normalized.salary_min}-{normalized.salary_max}"
                ),
                url=normalized.url,
                source=normalized.source,
            )

            self.repo.save(job)

            added += 1

        return {
            "new_jobs_added": added,
            "total_jobs": self.repo.count(),
        }