"""
Milestone 4: Embed chunks and store in ChromaDB.

Reads documents/chunks.json, encodes every chunk with all-MiniLM-L6-v2,
and upserts into a persistent ChromaDB collection with metadata:
  - source_id          : integer ID from planning.md source table
  - source_url         : original URL or local file path
  - source_description : human-readable source label
  - position           : zero-based chunk index within that source

Re-running is safe — upsert overwrites by chunk_id.
"""

import json
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "documents/chunks.json"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "grinnell_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def main() -> None:
    chunks_file = Path(CHUNKS_PATH)
    if not chunks_file.exists():
        sys.exit(f"ERROR: {CHUNKS_PATH} not found — run ingest.py first.")

    chunks = json.loads(chunks_file.read_text(encoding="utf-8"))
    if not chunks:
        sys.exit("ERROR: chunks.json is empty — run ingest.py first.")

    print(f"Loaded {len(chunks)} chunks from {CHUNKS_PATH}")

    print(f"Loading embedding model '{EMBEDDING_MODEL}' ...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [c["text"] for c in chunks]
    print("Embedding chunks ...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    ids = [c["chunk_id"] for c in chunks]
    metadatas = [
        {
            "source_id": c["source_id"],
            "source_url": c["source_url"],
            "source_description": c["source_description"],
            "position": int(c["chunk_id"].split("_chunk")[1]),
        }
        for c in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
    )

    print(f"\nDone. {len(chunks)} chunks stored in ChromaDB collection '{COLLECTION_NAME}'")
    print(f"Persisted to {CHROMA_PATH}/")


if __name__ == "__main__":
    main()
