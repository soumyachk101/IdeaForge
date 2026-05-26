"""Centralized configuration for IdeaForge."""
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / ".ideaforge_data"

CONFIG = {
    # LLM
    "llm_provider": os.getenv("LLM_PROVIDER", "ollama"),
    "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "ollama_model": os.getenv("OLLAMA_MODEL", "deepseek-coder-v2"),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    # Reddit
    "reddit_client_id": os.getenv("REDDIT_CLIENT_ID", ""),
    "reddit_client_secret": os.getenv("REDDIT_CLIENT_SECRET", ""),
    "reddit_user_agent": os.getenv("REDDIT_USER_AGENT", "IdeaForge/0.1.0"),
    # Product Hunt
    "product_hunt_token": os.getenv("PRODUCT_HUNT_TOKEN", ""),
    # RAG
    "chroma_path": os.getenv("CHROMA_PATH", str(DATA_DIR / "chroma")),
    "embedding_model": os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
    # Server
    "api_host": os.getenv("API_HOST", "127.0.0.1"),
    "api_port": int(os.getenv("API_PORT", "8000")),
    "frontend_url": os.getenv("FRONTEND_URL", "http://localhost:3000"),
}
