from fastapi import APIRouter, HTTPException

from app.agents.resume_match_agent import ResumeMatchAgent
from app.services.state import state

router = APIRouter(
    prefix="/ai",
    tags=["AI Matching"],
)


@router.get("/match")
def ai_match():

    if state.resume is None:
        raise HTTPException(
            status_code=400,
            detail="Resume not analyzed."
        )

    if not state.jobs:
        raise HTTPException(
            status_code=400,
            detail="Search jobs first."
        )

    agent = ResumeMatchAgent()

    results = []

    for job in state.jobs:

        analysis = agent.match(
            state.resume,
            job,
        )

        results.append(
            {
                "job": job,
                "analysis": analysis,
            }
        )

    return results