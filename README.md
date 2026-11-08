# PDF Report Processor & Generator

## Overview
This project is a robust, automated Python pipeline designed to process uploaded PDF reports, dynamically classify their type, extract relevant data, and generate newly formatted, standardized PDF reports. It is built to handle both digital PDFs and scanned documents using OCR fallback.

## System Architecture
The project follows a clean architecture based on the **Separation of Concerns (SoC)** principle, divided into distinct processing stations:

1. **Extractor (`core/extractor.py`)**: Reads the input PDF. Attempts standard text extraction first (`pdfplumber`), and falls back to Tesseract OCR for scanned images.
2. **Classifier / Factory (`core/factory.py`)**: Normalizes the extracted text and detects the report type based on flexible, bidirectional keyword matching. It then routes the data to the appropriate processing components.
3. **Data Builders (`data_builders/`)**: Parses the raw text into structured data models depending on the report type (e.g., calculating hours, structuring table rows).
4. **Renderers (`renderers/`)**: Takes the structured data models and generates a brand new, visually accurate PDF report using `reportlab`.

## Key Features
* **Robust Text Extraction:** Handles standard digital PDFs and uses Tesseract OCR (`--psm 6`) specifically tuned for Hebrew text and tables.
* **Smart Classification:** Identifies report types even with common OCR typos or reversed Hebrew text.
* **Modular Design:** Easy to add new report types without altering existing core logic.
* **Accurate PDF Generation:** Reconstructs complex tables (e.g., 11-column layouts, summary tables) with right-to-left (RTL) alignment and custom Hebrew fonts.
* **Safe File Handling:** Automatically appends unique timestamps to generated reports to prevent accidental data overwriting.

## Prerequisites
* **Python 3.10+**
* **Tesseract-OCR:** Must be installed on the system with the Hebrew language data package (`heb.traineddata`).

## Dependencies
* `pdfplumber` (for PDF text extraction)
* `pytesseract` (for OCR fallback)
* `reportlab` (for PDF generation)

## Project Structure
```text
project_root/
├── core/
│   ├── extractor.py      # PDF text and OCR extraction
│   ├── factory.py        # Report type classification and routing
│   └── models.py         # Data classes (Domain models)
├── data_builders/
│   ├── builder_type_a.py # Logic for parsing and calculating Type A reports
│   └── builder_type_b.py # Logic for parsing and calculating Type B reports
├── renderers/
│   ├── renderer_type_a.py # PDF drawing logic for Type A
│   └── renderer_type_b.py # PDF drawing logic for Type B
├── templates/
│   └── arial.ttf         # Custom Hebrew font for ReportLab
├── output/               # Directory for generated reports
├── main.py               # Main execution script (Orchestrator)
└── README.md             # Project documentation
```

## Usage
Run the main script via the command line, providing the path to the target PDF file as an argument:

```bash
python main.py <path_to_input_pdf_file>
```

**Example:**
```bash
python main.py data/inputs/sample_report.pdf
```

Upon successful execution, the system will output the detected report type and save the newly generated PDF in the `output/` directory with a timestamped filename (e.g., `generated_report_workplace_a_20261104_123000.pdf`).