import os

from dotenv import load_dotenv
from google import genai

load_dotenv() 

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
_model = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

PROMPT_TEMPLATE = """Sen bir belge asistanısın. Soruyu SADECE aşağıdaki belge parçalarına dayanarak cevapla.
Cevap parçalarda yoksa "Belgede bu bilgiyi bulamadım." de, (cevap bulamazsan bunu da o dilde söyle) tahmin yürütme.
Cevabın sonunda kullandığın sayfa numaralarını yaz.
Soru hangi dilde sorulduysa o dilde cevap ver.

BELGE PARÇALARI:
{context}

SORU: {question}

CEVAP:"""


def generate_answer(question: str, hits: list[dict]) -> str:
    """Bulunan chunk'ları bağlam olarak verip LLM'den cevap üretir."""
    context = "\n\n".join(f"[Sayfa {h['page']}]\n{h['text']}" for h in hits)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    response = _client.models.generate_content(model=_model, contents=prompt)
    return response.text