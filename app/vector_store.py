import chromadb

from app.embedder import embed_texts

# Veriler chroma_db klasörüne kaydedilir
_client = chromadb.PersistentClient(path="chroma_db")
_collection = _client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"},  # benzerlik ölçüsü: cosine
)


def add_chunks(chunks: list[dict], source: str) -> int:
    """Chunk'ları embedding'leriyle birlikte veritabanına ekler."""
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)

    ids = [f"{source}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "page": c["page"]} for c in chunks]

    # upsert: aynı id varsa günceller, yoksa ekler (tekrar çalıştırınca kopya oluşmaz)
    _collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(chunks)


def search(query: str, top_k: int = 3) -> list[dict]:
    """Soruya en yakın chunk'ları döndürür."""
    query_embedding = embed_texts([query])[0]

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    hits = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "text": text,
            "page": metadata["page"],
            "source": metadata["source"],
            "score": round(1 - distance, 3),  # cosine mesafesini benzerliğe çevir
        })
    return hits