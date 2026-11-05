from app.embedder import embed_texts

sentences = [
    "I fixed SQL bugs in the database",
    "I debugged database queries",
    "I like eating pizza",
]

vectors = embed_texts(sentences)

print(f"Vektör sayısı: {len(vectors)}")
print(f"Her vektörün boyutu: {len(vectors[0])}")
print(f"İlk vektörün ilk 5 sayısı: {vectors[0][:5]}")

# Benzerlik hesabı (cosine similarity)
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    return dot / (norm_a * norm_b)

print(f"\nSQL vs debug: {cosine(vectors[0], vectors[1]):.2f}")
print(f"SQL vs pizza: {cosine(vectors[0], vectors[2]):.2f}")