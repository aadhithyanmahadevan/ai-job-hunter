import shutil
import traceback
from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from app.providers.gemini_provider import GeminiProvider
from app.resumes.parser import ResumeParser
from app.services.state import state
from app.services.resume_cache import ResumeCache

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
        "success": True,
        "message": "Resume uploaded successfully.",
        "filename": file.filename,
        "path": str(filepath),
    }


@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):

    try:

        # ----------------------------------------
        # Save uploaded resume
        # ----------------------------------------

        filepath = UPLOAD_DIR / file.filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ----------------------------------------
        # Extract text
        # ----------------------------------------

        parser = ResumeParser()

        resume_text = parser.extract_text(str(filepath))

        if not resume_text.strip():

            return {
                "success": False,
                "error": "Unable to extract text from the resume."
            }

        # ----------------------------------------
        # AI Analysis
        # ----------------------------------------

        resume_hash = ResumeCache.get_hash(
            resume_text
        )

        if ResumeCache.exists(resume_hash):

            print("Loaded resume from cache")

            result = ResumeCache.load(
                resume_hash
            )

        else:

            print("Analyzing resume with Gemini")

            ai = GeminiProvider()

            result = ai.analyze_resume(
                resume_text
            )

            ResumeCache.save(
                resume_hash,
                result
            )

        state.resume = result

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        print("=" * 80)
        print("Resume Analysis Error")
        print("=" * 80)
        traceback.print_exc()

        error = str(e)

        # ----------------------------------------
        # Gemini Quota
        # ----------------------------------------

        if "429" in error or "RESOURCE_EXHAUSTED" in error:

            return {
                "success": False,
                "error": "Gemini API quota exceeded.",
                "message": "Please wait a few seconds and try again, or use a different API key.",
                "retry": True
            }

        # ----------------------------------------
        # Invalid API Key
        # ----------------------------------------

        if "API_KEY" in error.upper():

            return {
                "success": False,
                "error": "Invalid Gemini API Key."
            }

        # ----------------------------------------
        # Generic Error
        # ----------------------------------------

        return {
            "success": False,
            "error": error
        }