"""
FastAPI application entrypoint.

OWNERSHIP NOTE (team boundary):
Wires up the complete backend pipeline for AI ArchRedTeam:
- Core State: Projects, Architecture, Risks
- Vision/Upload: Diagram image analysis
- Multi-Agent Debate: Cross-agent architectural critique
- Defense & Evaluation: Student response grading and corrected architecture
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import all models before init_db() to ensure SQLAlchemy registers table metadata
import app.models  # noqa: F401
from app.api.routes import architecture, debate, evaluation, projects, risks, upload
from app.core.config import settings
from app.core.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_archredteam")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all database tables on startup (idempotent)."""
    init_db()
    logger.info("Database initialized at %s", settings.DATABASE_URL)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Database & State backend for AI ArchRedTeam. Provides CRUD for "
        "Projects, ArchitectureSpecs, RiskAssessments, DebateReports, and "
        "DefenseEvaluations, exposing the complete end-to-end evaluation pipeline."
    ),
    lifespan=lifespan,
)

# Permissive CORS for hackathon convenience (frontend may run on any port).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Global error handlers ---------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    safe_errors = [
        {
            "loc": list(err.get("loc", [])),
            "msg": err.get("msg"),
            "type": err.get("type"),
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Invalid request data.", "errors": safe_errors},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled server error on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred."},
    )


# --- Routers -------------------------------------------------------------
app.include_router(projects.router, prefix=settings.API_PREFIX)
app.include_router(architecture.router, prefix=settings.API_PREFIX)
app.include_router(risks.router, prefix=settings.API_PREFIX)
app.include_router(upload.router, prefix=settings.API_PREFIX)
app.include_router(debate.router, prefix=settings.API_PREFIX)
app.include_router(evaluation.router, prefix=settings.API_PREFIX)


# --- Health check endpoints ---------------------------------------------
@app.get("/", tags=["Health"], summary="Root health check")
def root() -> dict:
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"], summary="Service health status")
def health() -> dict:
    return {"status": "ok"}