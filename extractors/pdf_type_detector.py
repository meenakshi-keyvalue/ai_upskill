import fitz  # PyMuPDF

def is_text_pdf(file_path):
    doc = fitz.open(file_path)
    for page in doc:
        if page.get_text().strip():
            return True
    return False
