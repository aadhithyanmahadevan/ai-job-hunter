from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.search_agent import JobSearchAgent
from app.database.dependencies import get_db
from app.database.repository import JobRepository

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get("/search")
def search_jobs(db: Session = Depends(get_db)):

    agent = JobSearchAgent(db)

    return agent.search()


@router.get("/")
def get_jobs(db: Session = Depends(get_db)):

    repo = JobRepository(db)

    return repo.get_all()