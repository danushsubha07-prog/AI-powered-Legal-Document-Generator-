from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from legalese_api.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI backend for LegalEase AI-assisted legal document drafting.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to LegalEase AI Legal Document Generator API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "LegalEase API",
        "ai_configured": bool(settings.gemini_api_key),
        "demo_mode": settings.demo_mode,
        "model": settings.gemini_model,
    }
