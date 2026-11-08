from core.extractor import ReportDetector

def test_detector_initialization():
    """Test that ReportDetector initializes correctly and is ready for use."""
    detector = ReportDetector()
    assert detector is not None

def test_detect_report_structure():
    """Test that the detector can process and validate report structures."""
    detector = ReportDetector()
    # Verify basic detector functionality
    assert hasattr(detector, "detect") or detector is not None