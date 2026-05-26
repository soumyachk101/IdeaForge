"""IdeaForge FastAPI Backend."""
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ideaforge")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting IdeaForge API...")
    logger.info(f"  LLM provider: {CONFIG['llm_provider']}")
    logger.info(f"  ChromaDB path: {CONFIG['chroma_path']}")
    yield
    logger.info("Shutting down IdeaForge API...")


app = FastAPI(
    title="IdeaForge API",
    description="Multi-Agent Micro-SaaS Idea Discovery Engine",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CONFIG["frontend_url"], "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
from api.routes import health, ideas, trends, rag

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(ideas.router, prefix="/api", tags=["ideas"])
app.include_router(trends.router, prefix="/api", tags=["trends"])
app.include_router(rag.router, prefix="/api", tags=["rag"])


@app.get("/")
async def root():
    return {
        "name": "IdeaForge",
        "description": "Multi-Agent Micro-SaaS Idea Discovery Engine",
        "docs": "/docs",
    }


def main():
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=CONFIG["api_host"],
        port=CONFIG["api_port"],
        reload=True,
    )


if __name__ == "__main__":
    main()
