from fastapi import APIRouter, HTTPException

from app.services.state import state
from app.services.matcher import AIMatcher

router = APIRouter(
    prefix="/match",
    tags=["Match"],
)


@router.post("/")
def calculate_match(job: dict):

    if state.resume is None:
        raise HTTPException(
            status_code=400,
            detail="Resume not analyzed yet."
        )

    result = AIMatcher.calculate_match(
        state.resume,
        job.get("skills", [])
    )

    return result