from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.agents.search_agent import JobSearchAgent
from app.database.session import get_db

from app.core.logger import logger

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get("/search")
def search_jobs(
    db: Session = Depends(get_db),
):

    try:

        agent = JobSearchAgent(db)

        result = agent.search()

        logger.info("Searching jobs...")

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
