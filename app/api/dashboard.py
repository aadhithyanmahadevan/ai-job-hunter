from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db

from app.database.resume_repository import ResumeRepository
from app.models.user import User

from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/{resume_id}")
def dashboard_summary(
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

    service = DashboardService(db)

    return service.get_dashboard(resume_id)
