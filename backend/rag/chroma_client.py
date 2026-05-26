"""ChromaDB client for RAG storage with multiple collections."""
import chromadb
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

from config import CONFIG

logger = logging.getLogger("ideaforge.rag")

COLLECTIONS = ["pain_points", "monetization_frameworks", "startup_case_studies", "trends"]


class ChromaClient:
    def __init__(self, path: Optional[str] = None):
        path = path or CONFIG["chroma_path"]
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.path),
            settings=chromadb.Settings(anonymized_telemetry=False, allow_reset=True),
        )

        self.collections: Dict[str, chromadb.Collection] = {}
        for name in COLLECTIONS:
            self.collections[name] = self.client.get_or_create_collection(
                name=name, metadata={"hnsw:space": "cosine"}
            )

        logger.info(f"ChromaDB initialized at {self.path}")

    def add(
        self,
        collection: str,
        doc_id: str,
        text: str,
        embedding: List[float],
        metadata: Dict[str, Any],
    ):
        self.collections[collection].add(
            ids=[doc_id], documents=[text], embeddings=[embedding], metadatas=[metadata]
        )

    def add_batch(
        self,
        collection: str,
        doc_ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
    ):
        self.collections[collection].add(
            ids=doc_ids, documents=texts, embeddings=embeddings, metadatas=metadatas
        )

    def query(
        self,
        collection: str,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict]:
        try:
            return self.collections[collection].query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where,
            )
        except Exception as e:
            logger.error(f"Query failed on {collection}: {e}")
            return None

    def count(self, collection: str) -> int:
        return self.collections[collection].count()

    def get_all(self, collection: str, limit: int = 100) -> Dict[str, Any]:
        """Get all documents from a collection (for BM25 indexing or browsing)."""
        return self.collections[collection].get(
            limit=limit, include=["documents", "metadatas"]
        )

    def purge(self, collection: str):
        self.client.delete_collection(collection)
        self.collections[collection] = self.client.get_or_create_collection(
            name=collection, metadata={"hnsw:space": "cosine"}
        )

    def purge_all(self):
        self.client.reset()
        self.collections.clear()
        for name in COLLECTIONS:
            self.collections[name] = self.client.get_or_create_collection(
                name=name, metadata={"hnsw:space": "cosine"}
            )
        logger.info("All collections purged.")
