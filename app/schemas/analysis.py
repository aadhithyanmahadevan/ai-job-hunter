from datetime import datetime

from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    ats_score: int
    strengths: list[str]
    missing_skills: list[str]
    suggestions: list[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class AnalyzeResumeResponse(BaseModel):
    success: bool
    resume_id: int
    analysis: dict