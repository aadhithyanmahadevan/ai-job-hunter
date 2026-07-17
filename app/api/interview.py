from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.providers.gemini_provider import GeminiProvider

router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)


class InterviewRequest(BaseModel):
    description: str


@router.post("/questions")
def interview_questions(request: InterviewRequest):

    try:

        ai = GeminiProvider()

        result = ai.generate_interview_questions(
            request.description
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )