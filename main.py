import sys
from pathlib import Path
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Import the newly separated core components
from core.extractor import PDFTextExtractor
from core.factory import ReportFactory
from core.models import ReportType


def main(input_file_path: str):
    """
    Main execution script for processing an uploaded report file.
    Extracts text, identifies the report type via Factory, and generates a new PDF.
    """
    input_path = Path(input_file_path)

    # 1. Validate input file existence
    if not input_path.exists():
        print(f"Error: Input file '{input_file_path}' not found.")
        return

    # 2. Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True, parents=True)

    # 3. Register custom Hebrew font (Arial) if available
    font_path = Path("templates/arial.ttf")
    font_name = 'Helvetica'  # Default fallback font

    if font_path.exists():
        try:
            pdfmetrics.registerFont(TTFont('Arial', str(font_path)))
            font_name = 'Arial'
        except Exception:
            print("Warning: Failed to load custom font, using default.")

    # 4. Extract text from the uploaded PDF using the Extractor
    extractor = PDFTextExtractor()
    clean_text = extractor.extract(input_path)

    # 5. Identify the report type using the Factory
    factory = ReportFactory()
    report_type = factory.identify_type(clean_text)
    print(f"Info: Detected report type '{report_type.value}' from input file.")

    if report_type == ReportType.UNKNOWN:
        print("Error: Unknown or unsupported report type detected.")
        return

    # 6. Retrieve appropriate Builder and Renderer, then generate the PDF
    try:
        # The factory provides the correct instances for the detected type
        builder, renderer = factory.get_components(report_type, font_name)
        data = builder.build()

        # Generate a unique timestamp to prevent file overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"generated_report_{report_type.value}_{timestamp}.pdf"

        # Render and save the final PDF
        renderer.render(data, output_file)
        print(f"Success! Report generated at: {output_file}")

    except ValueError as e:
        print(f"Error generating report components: {e}")


if __name__ == "__main__":
    # Check if a file path was passed via command line arguments
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        main(target_file)
    else:
        print("Error: Please provide an input file path. Usage: python main.py <file_path>")