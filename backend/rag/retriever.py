"""Hybrid retrieval: vector search + BM25 with Reciprocal Rank Fusion."""
from typing import List, Tuple, Dict, Any, Optional
import logging

from rank_bm25 import BM25Okapi
import numpy as np

logger = logging.getLogger("ideaforge.rag")


class HybridRetriever:
    def __init__(self, chroma_client, embedder, k: int = 60):
        self.chroma = chroma_client
        self.embedder = embedder
        self.k = k  # RRF constant
        # BM25 indexes per collection
        self._bm25: Dict[str, BM25Okapi] = {}
        self._doc_ids: Dict[str, List[str]] = {}
        self._corpus: Dict[str, List[str]] = {}

    def build_bm25_index(self, collection: str):
        """Build BM25 index from all documents in a collection."""
        data = self.chroma.get_all(collection, limit=10000)
        ids = data.get("ids", [])
        docs = data.get("documents", [])
        if not ids:
            logger.warning(f"No documents in '{collection}' for BM25 index")
            return
        tokenized = [doc.lower().split() for doc in docs]
        self._bm25[collection] = BM25Okapi(tokenized)
        self._doc_ids[collection] = ids
        self._corpus[collection] = docs
        logger.info(f"BM25 index built for '{collection}': {len(ids)} documents")

    def _rrf_fusion(
        self,
        vector_ids: List[str],
        keyword_ids: List[str],
        n_results: int,
    ) -> List[Tuple[str, float]]:
        """Reciprocal Rank Fusion of vector and keyword results."""
        scores: Dict[str, float] = {}
        for rank, doc_id in enumerate(vector_ids, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (self.k + rank)
        for rank, doc_id in enumerate(keyword_ids, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (self.k + rank)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n_results]

    def retrieve(
        self,
        collection: str,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Hybrid retrieval combining vector + BM25 search."""
        query_vec = self.embedder.embed(query)

        # Vector search
        vec_results = self.chroma.query(
            collection, query_vec, n_results=n_results * 2, where=where
        )
        vec_ids = vec_results.get("ids", [[]])[0] if vec_results else []

        # BM25 search
        keyword_ids = []
        if collection in self._bm25:
            tokenized = query.lower().split()
            scores = self._bm25[collection].get_scores(tokenized)
            top_indices = np.argsort(scores)[::-1][: n_results * 2]
            keyword_ids = [
                self._doc_ids[collection][i]
                for i in top_indices
                if scores[i] > 0
            ]

        # Fuse
        fused = self._rrf_fusion(vec_ids, keyword_ids, n_results)
        if not fused:
            return []

        # Fetch full documents
        fused_ids = [fid for fid, _ in fused]
        score_map = dict(fused)
        records = self.chroma.collections[collection].get(ids=fused_ids)

        results = []
        for doc_id in fused_ids:
            if doc_id in records.get("ids", []):
                idx = records["ids"].index(doc_id)
                results.append({
                    "id": doc_id,
                    "text": records["documents"][idx],
                    "metadata": records["metadatas"][idx] or {},
                    "score": score_map.get(doc_id, 0.0),
                })
        return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from rag.chroma_client import ChromaClient
    from rag.embedder import TextEmbedder

    chroma = ChromaClient()
    embedder = TextEmbedder()
    retriever = HybridRetriever(chroma, embedder)
    for col in ["pain_points", "monetization_frameworks", "startup_case_studies"]:
        retriever.build_bm25_index(col)

    results = retriever.retrieve("pain_points", "developer tools for log analysis", n_results=3)
    for r in results:
        print(f"[{r['score']:.4f}] {r['text'][:100]}...")
