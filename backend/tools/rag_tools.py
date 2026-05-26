"""CrewAI tools wrapping the RAG retriever."""
import json
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

# Lazy-initialized singletons (avoid reloading embedding model on every call)
_chroma = None
_embedder = None
_retriever = None


def _get_retriever():
    global _chroma, _embedder, _retriever
    if _retriever is None:
        from rag.chroma_client import ChromaClient
        from rag.embedder import TextEmbedder
        from rag.retriever import HybridRetriever

        _chroma = ChromaClient()
        _embedder = TextEmbedder()
        _retriever = HybridRetriever(_chroma, _embedder)
        for col in ["pain_points", "monetization_frameworks", "startup_case_studies"]:
            _retriever.build_bm25_index(col)
    return _retriever


class RAGQueryInput(BaseModel):
    query: str = Field(description="Search query for the RAG database")
    collection: str = Field(
        default="all",
        description="Collection to search: 'pain_points', 'monetization_frameworks', 'startup_case_studies', or 'all'"
    )
    n_results: int = Field(default=5, description="Number of results to return")


class RAGRetrieverTool(BaseTool):
    name: str = "retrieve_monetization_data"
    description: str = (
        "Searches the IdeaForge knowledge base for relevant monetization frameworks, "
        "user pain points, and startup case studies. Use this to find matching monetization "
        "strategies and validate ideas against historical data."
    )
    args_schema: Type[BaseModel] = RAGQueryInput

    def _run(self, query: str, collection: str = "all", n_results: int = 5) -> str:
        retriever = _get_retriever()

        collections = (
            ["pain_points", "monetization_frameworks", "startup_case_studies"]
            if collection == "all"
            else [collection]
        )

        all_results = {}
        for col in collections:
            results = retriever.retrieve(col, query, n_results=n_results)
            if results:
                all_results[col] = results

        # Format results for the agent
        output_parts = []
        for coll_name, docs in all_results.items():
            if docs:
                output_parts.append(f"\n=== {coll_name.upper()} ===")
                for i, doc in enumerate(docs, 1):
                    output_parts.append(f"\n{i}. [{doc['score']:.4f}] {doc['text'][:500]}")
                    if doc.get("metadata"):
                        meta = doc["metadata"]
                        if meta.get("title"):
                            output_parts.append(f"   Title: {meta['title']}")
                        if meta.get("category"):
                            output_parts.append(f"   Category: {meta['category']}")

        return "\n".join(output_parts) if output_parts else "No relevant data found in the knowledge base."
