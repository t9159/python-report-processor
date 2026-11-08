from data_builders.builder_type_a import BuilderTypeA
from data_builders.builder_type_b import BuilderTypeB
from core.models import ReportDataA, ReportDataB


def test_builder_type_a():
    """Test that BuilderTypeA correctly builds ReportDataA with records."""
    builder = BuilderTypeA()
    data = builder.build()

    assert isinstance(data, ReportDataA)
    assert len(data.records) > 0
    assert data.total_days is not None


def test_builder_type_b():
    """Test that BuilderTypeB correctly builds ReportDataB with valid structure."""
    builder = BuilderTypeB()
    data = builder.build()

    assert isinstance(data, ReportDataB)
