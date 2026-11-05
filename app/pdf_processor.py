from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """PDF'i okur, her sayfanın metnini sayfa numarasıyla birlikte döndürür."""
    reader = PdfReader(file_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()

        if text:  # boş sayfaları atla
            pages.append({"page": page_number, "text": text})

    return pages