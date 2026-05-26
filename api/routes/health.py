"""Health and stats endpoints."""
from fastapi import APIRouter
from api.models import HealthResponse, StatsResponse
from rag.chroma_client import ChromaClient
from config import CONFIG

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    chroma_status = "ok"
    try:
        client = ChromaClient()
        client.count("pain_points")
    except Exception as e:
        chroma_status = f"error: {e}"

    return HealthResponse(
        status="ok",
        version="0.1.0",
        llm_provider=CONFIG["llm_provider"],
        chroma_status=chroma_status,
    )


@router.get("/stats", response_model=StatsResponse)
async def stats():
    client = ChromaClient()
    return StatsResponse(
        pain_points_count=client.count("pain_points"),
        monetization_frameworks_count=client.count("monetization_frameworks"),
        startup_case_studies_count=client.count("startup_case_studies"),
        generated_ideas_count=0,
    )
