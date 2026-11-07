from sentence_transformers import SentenceTransformer

# Çok dilli model: Türkçe soru ile İngilizce belge arasında da eşleştirme yapabilir
_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
_model.max_seq_length = 256  


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Metin listesini vektör listesine çevirir."""
    return _model.encode(texts).tolist()