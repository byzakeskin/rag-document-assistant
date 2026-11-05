from sentence_transformers import SentenceTransformer

# Model bir kez yüklenir, her seferinde tekrar yüklenmez
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Metin listesini vektör listesine çevirir."""
    return _model.encode(texts).tolist()