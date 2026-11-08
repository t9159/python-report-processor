from abc import ABC, abstractmethod
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from bidi.algorithm import get_display
from core.models import ReportDataA, ReportDataB
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_path = Path("templates/arial.ttf")
if font_path.exists():
    pdfmetrics.registerFont(TTFont('Arial', str(font_path)))

class BaseRenderer(ABC):
    """Abstract base class providing shared logic and layout setup for all renderers."""

    def __init__(self, font_name: str = "Helvetica"):
        self.font_name = font_name

    def _rtl(self, text: str) -> str:
        """Processes text for Right-To-Left languages (Hebrew)."""
        if not text:
            return ""
        return get_display(str(text))

    def _init_canvas(self, output_path: str | Path):
        """Shared helper method to initialize canvas, size, and standard top margins."""
        pdf_canvas = canvas.Canvas(str(output_path), pagesize=A4)
        width, height = A4
        y_position = height - 30
        right_margin = width - 50
        return pdf_canvas, width, height, y_position, right_margin

    def _check_page_break(self, pdf_canvas, y_position: float, height: float, font_size: int = 10) -> float:
        """
        Checks if the current Y position has reached the bottom of the page.
        If so, creates a new page, resets the font, and returns the reset Y position.
        """
        if y_position < 50:
            pdf_canvas.showPage()
            pdf_canvas.setFont(self.font_name, font_size)
            return height - 50
        return y_position

    @abstractmethod
    def render(self, data: ReportDataA | ReportDataB, output_path: str | Path) -> None:
        """Must be implemented by all child renderers."""
        pass