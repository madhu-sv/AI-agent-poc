from docx import Document
from pdfminer.high_level import extract_text as extract_pdf_text
import fitz
import pytesseract
from PIL import Image


def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_text_from_pdf(file):
    text = extract_pdf_text(file)
    if text.strip():
        return text
    # fallback to OCR
    file.seek(0)
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    ocr_text = ""
    for page in pdf:
        img = Image.frombytes(
            "RGB", [page.rect.width, page.rect.height], page.get_pixmap().samples
        )
        ocr_text += pytesseract.image_to_string(img)
    return ocr_text


def extract_text_from_cv(file):
    ext = file.name.split(".")[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(file)
    elif ext == "docx":
        return extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file format.")
