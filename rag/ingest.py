"""Document ingestion pipeline - chunks, embeds, and stores documents in ChromaDB."""
import json
import uuid
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from rag.embedder import TextEmbedder
from rag.chroma_client import ChromaClient

logger = logging.getLogger("ideaforge.rag.ingest")

SEED_DIR = Path(__file__).parent / "seed_data"


def chunk_text(text: str, max_tokens: int = 500, overlap: int = 50) -> List[str]:
    """Simple word-based chunking with overlap."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + max_tokens
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks


def ingest_seed_data(embedder=None, client=None):
    """Ingests all seed data files into ChromaDB."""
    embedder = embedder or TextEmbedder()
    client = client or ChromaClient()

    for collection_name, filename in [
        ("monetization_frameworks", "monetization_frameworks.json"),
        ("pain_points", "pain_points.json"),
        ("startup_case_studies", "startup_case_studies.json"),
    ]:
        filepath = SEED_DIR / filename
        if not filepath.exists():
            logger.warning(f"Seed file not found: {filepath}")
            continue

        with open(filepath) as f:
            documents = json.load(f)

        doc_ids = []
        texts = []
        metadatas = []

        for doc in documents:
            text = doc.get("content", doc.get("description", doc.get("text", "")))
            if not text:
                continue
            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):
                doc_id = f"{doc.get('id', str(uuid.uuid4()))}_chunk{i}"
                metadata = {
                    "source": doc.get("source", "seed"),
                    "category": doc.get("category", ""),
                    "title": doc.get("title", ""),
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                }
                for key in ["framework", "niche", "pricing", "revenue", "tech_stack"]:
                    if key in doc:
                        metadata[key] = str(doc[key])

                doc_ids.append(doc_id)
                texts.append(chunk)
                metadatas.append(metadata)

        if texts:
            embeddings = embedder.embed_batch(texts)
            client.add_batch(collection_name, doc_ids, texts, embeddings, metadatas)
            logger.info(f"Ingested {len(texts)} chunks into {collection_name}")


# Alias for api/routes/rag.py
def ingest_all(reset: bool = False):
    """Ingest all seed data. Optionally reset collections first."""
    embedder = TextEmbedder()
    client = ChromaClient()
    if reset:
        client.purge_all()
    ingest_seed_data(embedder=embedder, client=client)


def ingest_document(collection: str, text: str, metadata: Optional[Dict[str, Any]] = None):
    """Ingest a single document at runtime."""
    embedder = TextEmbedder()
    client = ChromaClient()
    doc_id = f"api_{uuid.uuid4().hex[:12]}"
    embedding = embedder.embed(text)
    client.add(collection, doc_id, text, embedding, metadata or {})
    return doc_id


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import sys
    reset = "--reset" in sys.argv
    ingest_all(reset=reset)
    print("Seed data ingestion complete!")
