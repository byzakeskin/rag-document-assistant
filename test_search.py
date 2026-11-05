from app.pdf_processor import extract_text_from_pdf
from app.chunker import chunk_text
from app.vector_store import add_chunks, search

# 1. PDF'i oku, böl, veritabanına ekle
pages = extract_text_from_pdf("data/test.pdf")
chunks = chunk_text(pages)
count = add_chunks(chunks, source="test.pdf")
print(f"{count} chunk veritabanına eklendi\n")

# 2. Soru sor
questions = [
    "Which SQL work did he do?",
    "Has he worked on games?",
]

for q in questions:
    print(f"SORU: {q}")
    for hit in search(q):
        print(f"  [skor {hit['score']}, sayfa {hit['page']}] {hit['text'][:100]!r}")
    print()