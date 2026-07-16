from fastapi import APIRouter, HTTPException

from app.agents.matching_agent import MatchingAgent
from app.services.state import state

router = APIRouter(
    prefix="/match",
    tags=["AI Matching"],
)


@router.get("/")
def match_jobs():

    if state.resume is None:
        raise HTTPException(
            status_code=400,
            detail="Analyze a resume first."
        )

    if not state.jobs:
        raise HTTPException(
            status_code=400,
            detail="Search jobs first."
        )

    agent = MatchingAgent()

    return agent.match_jobs(
        state.resume,
        state.jobs,
    )