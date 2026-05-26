"""RAG query, ingest, and seed data endpoints."""
import uuid
import logging
from fastapi import APIRouter

from api.models import RAGQueryRequest, RAGQueryResponse
from rag.chroma_client import ChromaClient
from rag.embedder import TextEmbedder
from rag.retriever import HybridRetriever
from rag.ingest import chunk_text, ingest_all

router = APIRouter()
logger = logging.getLogger("ideaforge.api.rag")

_chroma = None
_embedder = None
_retriever = None


def _get_components():
    global _chroma, _embedder, _retriever
    if _chroma is None:
        _chroma = ChromaClient()
        _embedder = TextEmbedder()
        _retriever = HybridRetriever(_chroma, _embedder)
        for col in ["pain_points", "monetization_frameworks", "startup_case_studies"]:
            _retriever.build_bm25_index(col)
    return _chroma, _embedder, _retriever


@router.post("/rag/query")
async def rag_query(request: RAGQueryRequest):
    """Query the RAG knowledge base."""
    chroma, embedder, retriever = _get_components()

    collections = (
        ["pain_points", "monetization_frameworks", "startup_case_studies"]
        if request.collection == "all"
        else [request.collection]
    )

    all_results = {}
    for col in collections:
        try:
            results = retriever.retrieve(col, request.query, n_results=request.n_results)
            if results:
                all_results[col] = results
        except Exception as e:
            logger.warning(f"RAG query failed for '{col}': {e}")

    return {"results": all_results}


@router.post("/rag/ingest")
async def rag_ingest():
    """Ingest seed data into the RAG knowledge base."""
    try:
        ingest_all()
        chroma, _, _ = _get_components()
        counts = {
            col: chroma.count(col)
            for col in ["pain_points", "monetization_frameworks", "startup_case_studies"]
        }
        return {"message": f"Seed data ingested successfully", "counts": counts}
    except Exception as e:
        logger.error(f"Seed ingestion failed: {e}")
        return {"message": f"Ingestion failed: {e}"}


@router.post("/rag/ingest/seed")
async def rag_ingest_seed(reset: bool = False):
    """Ingest seed data with optional reset."""
    try:
        if reset:
            chroma = ChromaClient()
            chroma.purge_all()
            logger.info("Purged all ChromaDB collections")

        ingest_all()
        chroma, _, _ = _get_components()
        counts = {
            col: chroma.count(col)
            for col in ["pain_points", "monetization_frameworks", "startup_case_studies"]
        }
        return {"message": f"Seed data ingested successfully", "counts": counts}
    except Exception as e:
        logger.error(f"Seed ingestion failed: {e}")
        return {"message": f"Ingestion failed: {e}"}


@router.get("/rag/browse/{collection}")
async def rag_browse(collection: str, limit: int = 20):
    """Browse documents in a RAG collection."""
    chroma, _, _ = _get_components()
    if collection not in chroma.collections:
        return {"error": f"Unknown collection: {collection}"}

    data = chroma.get_all(collection, limit=limit)
    docs = data.get("documents", [])
    metas = data.get("metadatas", [])
    results = []
    for i, (doc, meta) in enumerate(zip(docs, metas)):
        results.append({"index": i, "text": doc[:500], "metadata": meta})
    return {"collection": collection, "count": len(results), "documents": results}
