from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.database.base import Base
from app.database.session import engine

# Register all SQLAlchemy models
import app.models

from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.interview import router as interview_router
from app.api.jobs import router as jobs_router
from app.api.match import router as match_router
from app.api.resume import router as resume_router
from app.api.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup tasks.
    """
    Base.metadata.create_all(bind=engine)

    yield

    """
    Shutdown tasks.
    """
    # Close connections, clear cache, etc. if needed


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


# -------------------------------------------------
# CORS
# -------------------------------------------------

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


# -------------------------------------------------
# API Routers
# -------------------------------------------------

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(match_router)
app.include_router(dashboard_router)
app.include_router(interview_router)


# -------------------------------------------------
# Root
# -------------------------------------------------

@app.get(
    "/",
    tags=["System"],
)
def home():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get(
    "/health",
    tags=["System"],
)
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }