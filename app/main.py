from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.core.exceptions import NotFoundException
from app.core.logging import setup_logging

# Register all SQLAlchemy models
import app.models

# API Routers
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.api.interview import router as interview_router
from app.api.jobs import router as jobs_router
from app.api.match import router as match_router
from app.api.resume import router as resume_router
from app.api.users import router as users_router
from app.core.middleware import RequestLoggingMiddleware
from app.core.error_handlers import register_exception_handlers

# -------------------------------------------------
# Logging
# -------------------------------------------------

setup_logging()
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Lifespan
# -------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup tasks.
    """
    logger.info("🚀 Starting AI Job Hunter API")

    yield

    """
    Shutdown tasks.
    """
    logger.info("🛑 Shutting down AI Job Hunter API")


# -------------------------------------------------
# FastAPI App
# -------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

register_exception_handlers(app)

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

app.add_middleware(RequestLoggingMiddleware)

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
app.include_router(health_router)

# -------------------------------------------------
# Root Endpoint
# -------------------------------------------------


@app.get("/", tags=["System"])
async def home():
    logger.info("Root endpoint accessed")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }