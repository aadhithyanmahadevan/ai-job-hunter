from pydantic import BaseModel


class JobResponse(BaseModel):
    title: str
    company: str
    location: str
    description: str
    salary: str
    url: str
    source: str
    skills: list[str]


class JobSearchResponse(BaseModel):
    new_jobs_added: int
    total_jobs: int
    jobs: list[JobResponse]