from pathlib import Path
import shutil

from fastapi import UploadFile

from app.core.logger import logger
from app.providers.gemini_provider import GeminiProvider
from app.resumes.parser import ResumeParser
from app.services.resume_cache import ResumeCache

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class ResumeService:

    parser = ResumeParser()
    ai = GeminiProvider()

    @staticmethod
    def save_file(file: UploadFile) -> tuple[str, str]:
        filename = file.filename
        filepath = UPLOAD_DIR / filename

        logger.info(f"Saving resume '{filename}'")

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return filename, str(filepath)

    @classmethod
    def extract_resume(cls, filepath: str):
        logger.info(f"Extracting text from '{filepath}'")
        return cls.parser.extract_text(filepath)

    @classmethod
    def analyze_resume(cls, text: str):
        logger.info("Sending resume to Gemini")
        return cls.ai.analyze_resume(text)

    @classmethod
    def analyze_with_cache(cls, text: str):

        resume_hash = ResumeCache.get_hash(text)

        if ResumeCache.exists(resume_hash):
            logger.info("Resume analysis cache hit")
            return ResumeCache.load(resume_hash)

        logger.info("Resume analysis cache miss")

        result = cls.ai.analyze_resume(text)

        ResumeCache.save(
            resume_hash,
            result,
        )

        logger.info("Resume analysis cached")

        return result
