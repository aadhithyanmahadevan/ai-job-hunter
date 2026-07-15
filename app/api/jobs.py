from fastapi import APIRouter

from app.agents.search_agent import JobSearchAgent

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/search")
def search_jobs():

    agent = JobSearchAgent()

    return agent.search()