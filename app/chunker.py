def chunk_text(
    pages: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[dict]:
    """Sayfa metinlerini satır sınırlarına göre örtüşmeli parçalara böler.
    Kelimeler ve satırlar ortadan kesilmez."""
    chunks = []

    for page in pages:
        lines = page["text"].split("\n")
        current: list[str] = []
        length = 0

        for line in lines:
            # Yeni satır sığmıyorsa mevcut parçayı kaydet
            if length + len(line) + 1 > chunk_size and current:
                chunks.append({"page": page["page"], "text": "\n".join(current).strip()})

                # Overlap: son satırlardan chunk_overlap karaktere kadarını taşı
                overlap: list[str] = []
                overlap_len = 0
                for prev in reversed(current):
                    if overlap_len + len(prev) > chunk_overlap:
                        break
                    overlap.insert(0, prev)
                    overlap_len += len(prev) + 1
                current = overlap
                length = overlap_len

            current.append(line)
            length += len(line) + 1

        if current:
            text = "\n".join(current).strip()
            if text:
                chunks.append({"page": page["page"], "text": text})

    return chunks