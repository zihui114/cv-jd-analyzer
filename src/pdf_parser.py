import fitz  # PyMuPDF

def parse_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    if not text.strip():
        raise ValueError(f"PDF 解析結果為空，建議改用 Markdown 或純文字版本：{path}")
    return text
