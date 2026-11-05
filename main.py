from fastapi import FastAPI

app = FastAPI(title="AI Document Assistant")

@app.get("/")
def home():
    return {"message": "RAG projesi çalışıyor!"}