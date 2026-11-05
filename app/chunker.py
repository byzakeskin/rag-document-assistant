def chunk_text(
    pages: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[dict]:
    """Sayfa metinlerini örtüşmeli parçalara böler.
    Her parçada hangi sayfadan geldiği bilgisi korunur."""
    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append({
                    "page": page["page"],
                    "text": chunk,
                })

            if end >= len(text):
                break
            start = end - chunk_overlap

    return chunks