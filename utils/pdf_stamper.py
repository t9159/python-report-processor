from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io
from pypdf import PdfReader, PdfWriter
from reportlab.platypus import Table
from reportlab.platypus.tableofcontents import TableStyle
from reportlab.lib import colors

class PDFStamper:
    """Utility class for adding official stamps or watermarks to generated PDFs."""

    @staticmethod
    def add_text_stamp(input_pdf_path: str | Path, output_pdf_path: str | Path,
                       stamp_text: str = "מאושר רשמית") -> None:
        """
        Adds an official stamp/watermark overlay to an existing PDF file.
        """
        input_path = Path(input_pdf_path)
        output_path = Path(output_pdf_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input PDF not found at: {input_path}")

        # 1. Create an in-memory PDF page containing the stamp graphic/text
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        width, height = A4

        # Set stamp appearance (e.g., a nice box with text at the bottom or corner)
        can.saveState()
        can.setFont("Arial", 10)
        can.setFillColor(colors.darkblue)

        # Draw a stamp box at the bottom-left of the page
        can.setStrokeColor(colors.darkblue)
        can.setLineWidth(1)
        can.rect(50, 40, 150, 25, stroke=1, fill=0)

        # Draw the text inside the stamp (reversing with bidi if needed, or direct text)
        can.drawString(60, 48, stamp_text)
        can.restoreState()

        can.save()
        packet.seek(0)

        # 2. Read the stamp overlay PDF and the original PDF
        stamp_pdf = PdfReader(packet)
        stamp_page = stamp_pdf.pages[0]

        reader = PdfReader(str(input_path))
        writer = PdfWriter()

        # 3. Merge the stamp onto every page of the original PDF
        for page in reader.pages:
            page.merge_page(stamp_page)
            writer.add_page(page)

        # 4. Write the final stamped PDF to disk
        with open(output_path, "wb") as output_file:
            writer.write(output_file)