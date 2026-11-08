from pathlib import Path
from data_builders.builder_type_a import BuilderTypeA
from renderers.renderer_type_a import RendererTypeA


def test_renderer_type_a_integration(temp_pdf_path):
    """Test integration of BuilderTypeA and RendererTypeA to generate a PDF file."""
    builder = BuilderTypeA()
    data = builder.build()

    renderer = RendererTypeA()
    renderer.render(data, temp_pdf_path)

    assert temp_pdf_path.exists()
    assert temp_pdf_path.stat().st_size > 0