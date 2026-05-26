"""Text embedding using sentence-transformers with MPS/CPU auto-detection."""
from sentence_transformers import SentenceTransformer
from typing import List
import torch
import logging

from config import CONFIG

logger = logging.getLogger("ideaforge.rag")


class TextEmbedder:
    def __init__(self, model_name: str = None):
        model_name = model_name or CONFIG["embedding_model"]
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"Initializing TextEmbedder ({model_name}) on {self.device}...")
        self.model = SentenceTransformer(model_name, device=self.device)
        logger.info(f"TextEmbedder loaded: {model_name}")

    def embed(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()
