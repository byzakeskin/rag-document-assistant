from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.chunker import chunk_text
from app.llm import generate_answer
from app.pdf_processor import extract_text_from_pdf
from app.vector_store import add_chunks, delete_source, search

app = FastAPI(title="AI Document Assistant")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/")
def home():
    return {"message": "RAG projesi çalışıyor!"}


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    """PDF yükler, metni çıkarır, parçalara böler ve veritabanına ekler."""
    filename = Path(file.filename or "").name  # klasör yolu içeren adlara karşı güvenlik
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyaları yüklenebilir.")

    file_path = DATA_DIR / filename
    file_path.write_bytes(file.file.read())

    try:
        pages = extract_text_from_pdf(str(file_path))
    except Exception:
        raise HTTPException(status_code=400, detail="PDF okunamadı, dosya bozuk olabilir.")

    if not pages:
        raise HTTPException(
            status_code=422,
            detail="PDF'ten metin çıkarılamadı (taranmış/fotoğraf PDF olabilir).",
        )

    chunks = chunk_text(pages)
    delete_source(filename)
    count = add_chunks(chunks, source=filename)

    return {"filename": filename, "pages": len(pages), "chunks": count}


@app.post("/ask")
def ask(request: AskRequest):
    """Soruya en alakalı parçaları bulur ve LLM ile cevap üretir."""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Soru boş olamaz.")

    hits = search(question, top_k=request.top_k)
    if not hits:
        return {"answer": "Henüz yüklenmiş bir belge yok.", "sources": []}

    try:
        answer = generate_answer(question, hits)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM hatası: {e}")

    sources = [
        {
            "source": h["source"],
            "page": h["page"],
            "score": h["score"],
            "preview": h["text"][:150],
        }
        for h in hits
    ]
    return {"answer": answer, "sources": sources}