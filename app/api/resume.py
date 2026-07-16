import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.providers.gemini_provider import GeminiProvider
from app.resumes.parser import ResumeParser
from app.services.state import state

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Resume uploaded successfully.",
        "filename": file.filename,
        "path": str(filepath),
    }


@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parser = ResumeParser()

    resume_text = parser.extract_text(str(filepath))

    ai = GeminiProvider()

    result = ai.analyze_resume(resume_text)

    # Save analyzed resume in memory
    state.resume = result

    return result