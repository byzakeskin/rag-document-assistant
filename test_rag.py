from app.vector_store import search
from app.llm import generate_answer

questions = [
    "Which SQL work did he do and at which company?",
    "Has he worked on games?",
    "Does he know Kubernetes?",  # CV'de yok, "bulamadım" demeli
]

for q in questions:
    hits = search(q, top_k=5)
    answer = generate_answer(q, hits)
    print(f"SORU: {q}")
    print(f"CEVAP: {answer}\n")