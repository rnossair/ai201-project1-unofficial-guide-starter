"""
Milestone 4: Retrieval.

retrieve(query, k) embeds the query with all-MiniLM-L6-v2 and returns the
top-k most relevant chunks from ChromaDB along with their source metadata.
"""

import sys
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "grinnell_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

_model: SentenceTransformer | None = None
_collection: chromadb.Collection | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection


def retrieve(query: str, k: int = 5) -> list[dict]:
    """
    Return the top-k chunks most relevant to query.

    Each result dict contains:
      text               : chunk text
      source_id          : integer source ID from planning.md
      source_url         : original URL or file path
      source_description : human-readable source label
      position           : chunk index within its source document
      score              : cosine distance (lower = more similar)
    """
    query_embedding = _get_model().encode(query).tolist()
    results = _get_collection().query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append(
            {
                "text": text,
                "source_id": meta["source_id"],
                "source_url": meta["source_url"],
                "source_description": meta["source_description"],
                "position": meta["position"],
                "score": round(dist, 4),
            }
        )
    return chunks


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is the social life like at Grinnell?"
    print(f"Query: {query}\n")

    results = retrieve(query, k=5)
    for i, r in enumerate(results, 1):
        print(f"[{i}] score={r['score']}  {r['source_description']}  (pos {r['position']})")
        print(f"     {r['text'][:200]}")
        print()
