from app.pdf_processor import extract_text_from_pdf

pages = extract_text_from_pdf("data/test.pdf")

print(f"Toplam sayfa: {len(pages)}")
print("--- İlk sayfanın ilk 500 karakteri ---")
print(pages[0]["text"][:500])