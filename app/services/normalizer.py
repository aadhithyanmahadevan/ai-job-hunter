from app.models.job_dto import JobDTO


def normalize_adzuna(job):

    return JobDTO(
        title=job.get("title", ""),
        company=job.get("company", {}).get("display_name", ""),
        location=job.get("location", {}).get("display_name", ""),
        description=job.get("description", ""),
        salary_min=job.get("salary_min"),
        salary_max=job.get("salary_max"),
        url=job.get("redirect_url", ""),
        source="Adzuna",
    )
