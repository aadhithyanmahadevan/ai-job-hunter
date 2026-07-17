from app.models.job import Job


class JobService:

    @staticmethod
    def create_job(
        title,
        company,
        location,
        description,
        salary,
        url,
        source,
    ):

        return Job(
            title=title,
            company=company,
            location=location,
            description=description,
            salary=salary,
            url=url,
            source=source,
        )
