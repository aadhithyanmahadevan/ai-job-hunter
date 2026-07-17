from pydantic import BaseModel


class MatchResponse(BaseModel):
    score: int

    strengths: list[str]

    missing_skills: list[str]

    matched_keywords: list[str]

    experience_match: str

    recommendation: str

    reasoning: str
