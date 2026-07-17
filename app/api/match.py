import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db

from app.database.resume_repository import ResumeRepository
from app.database.job_repository import JobRepository
from app.database.match_repository import MatchRepository

from app.models.match import Match
from app.models.user import User

from app.services.match_service import MatchService
from app.core.logger import logger


router = APIRouter(
    prefix="/match",
    tags=["AI Job Matching"],
)


@router.post("/")
def match_resume_to_job(
    resume_id: int,
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    resume_repo = ResumeRepository(db)
    job_repo = JobRepository(db)
    match_repo = MatchRepository(db)

    resume = resume_repo.get(resume_id)

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized",
        )

    job = job_repo.get(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    service = MatchService(db)

    result = service.analyze(
        resume.extracted_text,
        job.description,
    )

    match = Match(
        resume_id=resume.id,
        job_id=job.id,
        match_score=result.get("score", 0),
        matched_skills=json.dumps(
            result.get("strengths", [])
        ),
        missing_skills=json.dumps(
            result.get("missing_skills", [])
        ),
        recommendations=result.get(
            "recommendation",
            "",
        ),
        raw_json=json.dumps(result),
    )

    match_repo.create(match)

    return result


@router.post("/resume/{resume_id}")
def match_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    resume_repo = ResumeRepository(db)

    resume = resume_repo.get(resume_id)

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized",
        )

    service = MatchService(db)

    return service.match_resume(resume_id)


@router.get("/{resume_id}")
def get_match_history(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    resume_repo = ResumeRepository(db)
    match_repo = MatchRepository(db)

    resume = resume_repo.get(resume_id)

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized",
        )
    
    logger.info(
    f"Matching jobs for resume {resume_id}"
    )

    return match_repo.get_by_resume(resume_id)