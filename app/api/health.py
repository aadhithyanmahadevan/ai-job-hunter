from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import SessionLocal

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "AI Job Hunter",
        "version": "1.0.0",
    }


@router.get("/ready")
async def ready():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()

        return {
            "status": "ready",
            "database": "connected",
        }

    except Exception as e:
        return {
            "status": "not_ready",
            "database": "disconnected",
            "error": str(e),
        }