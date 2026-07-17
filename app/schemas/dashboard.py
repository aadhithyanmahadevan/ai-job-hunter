from pydantic import BaseModel


class DashboardResponse(BaseModel):
    resume_score: int

    jobs_analyzed: int

    average_match: float

    highest_match: int

    lowest_match: int

    top_missing_skills: list[str]
