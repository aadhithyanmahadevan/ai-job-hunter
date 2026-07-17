from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.jobs import router as jobs_router
from app.api.resume import router as resume_router
from app.api.match import router as match_router
from app.api.match_ai import router as ai_match_router
from app.api.dashboard import router as dashboard_router
from app.api.interview import router as interview_router

from app.config.settings import settings
from app.database.models import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Routers
# -------------------------
app.include_router(jobs_router)
app.include_router(resume_router)
app.include_router(match_router)
app.include_router(ai_match_router)
app.include_router(dashboard_router)
app.include_router(interview_router)

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