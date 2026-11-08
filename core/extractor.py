from pathlib import Path
import pdfplumber
import pytesseract

class PDFTextExtractor:
    """Handles reading text from a PDF file, with OCR fallback for scanned images."""

    @staticmethod
    def extract(pdf_path: str | Path) -> str:
        extracted_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) > 0:
                first_page = pdf.pages[0]

                # 1. Attempt standard text extraction
                extracted_text = first_page.extract_text() or ""

                # 2. Fallback to OCR if no text was found
                if not extracted_text.strip():
                    pil_image = first_page.to_image(resolution=300).original
                    extracted_text = pytesseract.image_to_string(pil_image, lang='heb', config='--psm 6') or ""

        # Clean punctuation and normalize text for easier identification later
        return extracted_text.replace(":", "").replace('"', '').replace("'", "")