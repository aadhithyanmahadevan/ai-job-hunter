from pathlib import Path
import shutil

from fastapi import APIRouter, File, UploadFile

from app.resumes.parser import ResumeParser
from app.resumes.extractor import ResumeExtractor

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parser = ResumeParser()
    text = parser.parse(str(destination))

    extractor = ResumeExtractor()
    skills = extractor.extract_skills(text)

    return {
        "filename": file.filename,
        "pages_text_length": len(text),
        "skills": skills
    }