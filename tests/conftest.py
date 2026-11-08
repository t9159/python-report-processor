import pytest
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

@pytest.fixture(scope="session", autouse=True)
def setup_global_font():
    """Register the Arial font globally for all tests before execution."""
    font_path = Path("templates/arial.ttf")
    if font_path.exists():
        try:
            pdfmetrics.registerFont(TTFont("Arial", str(font_path)))
        except Exception:
            pass

@pytest.fixture
def temp_pdf_path(tmp_path):
    """Provide a clean temporary file path for PDF integration tests."""
    return tmp_path / "sample_test_report.pdf"