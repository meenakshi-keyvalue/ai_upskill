import fitz
from PIL import Image
import pytesseract
import io

def extract_text_from_pdf_bytes(file_bytes):
    try:
        # Try text-based extraction first
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        has_text = False
        for page in doc:
            text = page.get_text()
            if text.strip():
                has_text = True
                full_text += text
        if has_text:
            return full_text
        else:
            # OCR fallback
            ocr_text = ""
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_text += pytesseract.image_to_string(img) + "\n"
            return ocr_text
    except Exception as e:
        return f"Error during extraction: {str(e)}"
