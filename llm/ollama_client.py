"""Ollama async client and CrewAI LLM wrapper."""
import httpx
import json
import logging
from typing import AsyncGenerator, Optional

from config import CONFIG

logger = logging.getLogger("ideaforge.llm")

OLLAMA_URL = CONFIG["ollama_base_url"] + "/api/generate"
DEFAULT_MODEL = CONFIG["ollama_model"]


async def stream_ollama(prompt: str, model: str = DEFAULT_MODEL) -> AsyncGenerator[str, None]:
    """Stream raw token chunks from Ollama."""
    payload = {"model": model, "prompt": prompt, "stream": True}
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                if response.status_code != 200:
                    yield f"Error: Ollama returned {response.status_code}"
                    return
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if "response" in chunk:
                        yield chunk["response"]
                    if chunk.get("done"):
                        break
    except Exception as e:
        logger.error(f"Ollama streaming failed: {e}")
        yield f"\n\n[error] Could not reach Ollama at {OLLAMA_URL}: {e}"


async def generate_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Non-streaming generation from Ollama."""
    chunks = []
    async for chunk in stream_ollama(prompt, model):
        chunks.append(chunk)
    return "".join(chunks)


def get_crewai_llm():
    """Returns a CrewAI-compatible LLM instance based on config."""
    provider = CONFIG["llm_provider"]

    if provider == "anthropic" and CONFIG.get("anthropic_api_key"):
        from crewai import LLM
        return LLM(
            model="anthropic/claude-sonnet-4-20250514",
            api_key=CONFIG["anthropic_api_key"],
        )

    # Default: Ollama
    from crewai import LLM
    return LLM(
        model=f"ollama/{CONFIG['ollama_model']}",
        base_url=CONFIG["ollama_base_url"],
    )
