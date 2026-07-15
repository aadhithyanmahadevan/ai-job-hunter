from fastapi import FastAPI

from app.api.jobs import router as jobs_router
from app.config.settings import settings
from app.database.models import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(jobs_router)


@app.get("/")
def home():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }