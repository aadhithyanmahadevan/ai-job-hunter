from pathlib import Path
import shutil

from fastapi import UploadFile
from app.resumes.parser import ResumeParser
from app.providers.gemini_provider import GeminiProvider
from app.services.resume_cache import ResumeCache

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class ResumeService:

    @staticmethod
    def save_file(file: UploadFile) -> tuple[str, str]:

        filename = file.filename

        filepath = UPLOAD_DIR / filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return filename, str(filepath)
    
    @staticmethod
    def extract_resume(filepath: str):

        parser = ResumeParser()

        return parser.extract_text(filepath)
    
    @staticmethod
    def analyze_resume(text: str):

        ai = GeminiProvider()

        return ai.analyze_resume(text)
    
    @staticmethod
    def analyze_with_cache(text: str):

        resume_hash = ResumeCache.get_hash(text)

        if ResumeCache.exists(resume_hash):

            return ResumeCache.load(resume_hash)

        ai = GeminiProvider()

        result = ai.analyze_resume(text)

        ResumeCache.save(
            resume_hash,
            result,
        )

        return result