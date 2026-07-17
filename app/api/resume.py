import json
import os

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.logger import logger
from app.database.analysis_repository import AnalysisRepository
from app.database.resume_repository import ResumeRepository
from app.database.session import get_db
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.models.user import User
from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


def validate_resume_owner(
    resume: Resume,
    current_user: User,
):
    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized",
        )


# --------------------------------------------------------
# Upload Resume
# --------------------------------------------------------


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.info(
        f"User '{current_user.email}' is uploading a resume."
    )

    resume_repo = ResumeRepository(db)

    try:
        filename, filepath = ResumeService.save_file(file)

        resume = Resume(
            user_id=current_user.id,
            filename=filename,
            file_path=filepath,
            extracted_text="",
            status="uploaded",
        )

        resume = resume_repo.create(resume)

        logger.info(
            f"Resume uploaded successfully. Resume ID: {resume.id}"
        )

        return {
            "success": True,
            "resume_id": resume.id,
            "filename": resume.filename,
            "message": "Resume uploaded successfully",
        }

    except Exception as e:
        logger.exception(
            f"Resume upload failed for user '{current_user.email}'."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# --------------------------------------------------------
# Analyze Resume
# --------------------------------------------------------


@router.post("/{resume_id}/analyze")
async def analyze_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume_repo = ResumeRepository(db)
    analysis_repo = AnalysisRepository(db)

    resume = resume_repo.get(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    validate_resume_owner(
        resume,
        current_user,
    )

    try:
        logger.info(
            f"Starting analysis for resume {resume.id}."
        )

        resume.status = "analyzing"
        resume_repo.update(resume)

        extracted_text = ResumeService.extract_resume(
            resume.file_path
        )

        resume.extracted_text = extracted_text
        resume_repo.update(resume)

        analysis_result = ResumeService.analyze_with_cache(
            extracted_text
        )

        resume.status = "completed"
        resume_repo.update(resume)

        analysis = ResumeAnalysis(
            resume_id=resume.id,
            ats_score=analysis_result.get("ats_score"),
            strengths=json.dumps(
                analysis_result.get("strengths", [])
            ),
            missing_skills=json.dumps(
                analysis_result.get("missing_skills", [])
            ),
            suggestions=json.dumps(
                analysis_result.get("suggestions", [])
            ),
            raw_json=json.dumps(analysis_result),
        )

        analysis_repo.create(analysis)

        logger.info(
            f"Analysis completed successfully for resume {resume.id}."
        )

        return {
            "success": True,
            "resume_id": resume.id,
            "analysis": analysis_result,
        }

    except Exception as e:
        logger.exception(
            f"Resume analysis failed for resume {resume_id}."
        )

        resume.status = "failed"
        resume_repo.update(resume)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume analysis failed: {str(e)}",
        )


# --------------------------------------------------------
# Get All Resumes
# --------------------------------------------------------


@router.get("/")
def get_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.info(
        f"Fetching resumes for user '{current_user.email}'."
    )

    resume_repo = ResumeRepository(db)

    return resume_repo.get_by_user(current_user.id)


# --------------------------------------------------------
# Get Resume Details
# --------------------------------------------------------


@router.get("/{resume_id}")
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.info(
        f"Fetching resume {resume_id}."
    )

    resume_repo = ResumeRepository(db)
    analysis_repo = AnalysisRepository(db)

    resume = resume_repo.get(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    validate_resume_owner(
        resume,
        current_user,
    )

    analysis = analysis_repo.get_by_resume(
        resume.id,
    )

    return {
        "resume": resume,
        "analysis": analysis,
    }


# --------------------------------------------------------
# Delete Resume
# --------------------------------------------------------


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume_repo = ResumeRepository(db)

    resume = resume_repo.get(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    validate_resume_owner(
        resume,
        current_user,
    )

    logger.info(
        f"Deleting resume {resume.id}."
    )

    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    resume_repo.delete(resume)

    logger.info(
        f"Resume {resume.id} deleted successfully."
    )

    return {
        "success": True,
        "message": "Resume deleted successfully",
    }