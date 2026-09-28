from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from ai_core.gemini_generator import GeminiDocumentGenerator
from config import get_settings

router = APIRouter()
settings = get_settings()
generator = GeminiDocumentGenerator(settings)


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=200)
    parties: str = Field(..., min_length=2, max_length=10000)
    terms: str = Field(..., min_length=2, max_length=15000)
    dates: str = Field(..., min_length=2, max_length=500)
    jurisdiction: str = Field(default="", max_length=500)
    language: str = Field(default="English", min_length=2, max_length=100)

    @field_validator("document_type", "parties", "terms", "dates", "jurisdiction", "language")
    @classmethod
    def strip_fields(cls, value: str) -> str:
        return value.strip()


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    total = sum(len(value) for value in [request.document_type, request.parties, request.terms, request.dates])
    if total > settings.max_input_chars:
        raise HTTPException(status_code=413, detail="Input is too large. Reduce the document details and try again.")

    try:
        result = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
            jurisdiction=request.jurisdiction,
            language=request.language,
        )
        return {
            "document": result.text,
            "mode": result.mode,
            "model": result.model,
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Document generation failed: {exc}") from exc
