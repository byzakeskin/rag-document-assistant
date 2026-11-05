from app.pdf_processor import extract_text_from_pdf
from app.chunker import chunk_text

pages = extract_text_from_pdf("data/test.pdf")
chunks = chunk_text(pages)

print(f"Toplam chunk: {len(chunks)}")
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i + 1} (sayfa {chunk['page']}, {len(chunk['text'])} karakter) ---")
    print(chunk["text"])