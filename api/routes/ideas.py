"""Idea generation endpoints with SSE streaming."""
import asyncio
import json
import uuid
import logging
from datetime import datetime
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from api.models import GenerateRequest

router = APIRouter()
logger = logging.getLogger("ideaforge.api.ideas")

# In-memory store for generated ideas
_ideas: dict = {}


@router.post("/ideas/generate")
async def generate_ideas(request: GenerateRequest):
    """SSE stream: runs the CrewAI pipeline and streams progress events."""
    from agents.crew import run_idea_pipeline

    idea_id = uuid.uuid4().hex[:12]
    niche = request.niche

    async def event_generator():
        yield {
            "event": "message",
            "data": json.dumps({"type": "start", "niche": niche, "id": idea_id}),
        }

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: run_idea_pipeline(niche=niche))

            _ideas[idea_id] = {
                "id": idea_id,
                "niche": niche,
                "content": result,
                "status": "completed",
                "created_at": datetime.now().isoformat(),
            }

            yield {
                "event": "message",
                "data": json.dumps({"type": "result", "id": idea_id, "content": result}),
            }

            yield {
                "event": "message",
                "data": json.dumps({"type": "done", "id": idea_id}),
            }

        except Exception as e:
            logger.error(f"Idea generation failed: {e}")
            yield {
                "event": "message",
                "data": json.dumps({"type": "error", "message": str(e)}),
            }

    return EventSourceResponse(event_generator())


@router.get("/ideas")
async def list_ideas():
    """List all generated ideas as summaries."""
    ideas = list(_ideas.values())
    ideas.sort(key=lambda x: x["created_at"], reverse=True)
    return [
        {
            "id": i["id"],
            "niche": i["niche"],
            "preview": i["content"][:200] + "..." if len(i.get("content", "")) > 200 else i.get("content", ""),
            "created_at": i["created_at"],
        }
        for i in ideas
    ]


@router.get("/ideas/{idea_id}")
async def get_idea(idea_id: str):
    """Get a generated idea by ID."""
    if idea_id not in _ideas:
        return {"error": "Idea not found"}
    idea = _ideas[idea_id]
    return {
        "id": idea["id"],
        "niche": idea["niche"],
        "content": idea["content"],
        "status": idea["status"],
        "created_at": idea["created_at"],
    }
