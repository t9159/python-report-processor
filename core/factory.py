from core.models import ReportType
from data_builders.builder_type_a import BuilderTypeA
from data_builders.builder_type_b import BuilderTypeB
from renderers.renderer_type_a import RendererTypeA
from renderers.renderer_type_b import RendererTypeB


class ReportFactory:
    """Identifies the report type from text and acts as a factory for builders and renderers."""

    TYPE_A_KEYWORDS = ["הנשר", "מקום", "125%"]
    TYPE_B_KEYWORDS = ["כרטיס", "עובד", "שעות", "לשעה", "תשלום"]

    @staticmethod
    def identify_type(clean_text: str) -> ReportType:
        """Determines the report type based on keywords in the text."""
        # Check for Type A keywords
        for keyword in ReportFactory.TYPE_A_KEYWORDS:
            if keyword in clean_text or keyword[::-1] in clean_text:
                return ReportType.WORKPLACE_A

        # Check for Type B keywords
        for keyword in ReportFactory.TYPE_B_KEYWORDS:
            if keyword in clean_text or keyword[::-1] in clean_text:
                return ReportType.WORKPLACE_B

        return ReportType.UNKNOWN

    @staticmethod
    def get_components(report_type: ReportType, font_name: str):
        """Returns the appropriate (Builder, Renderer) instances for the given report type."""
        if report_type == ReportType.WORKPLACE_A:
            return BuilderTypeA(), RendererTypeA(font_name=font_name)

        elif report_type == ReportType.WORKPLACE_B:
            return BuilderTypeB(), RendererTypeB(font_name=font_name)

        else:
            raise ValueError(f"No components mapped for report type: {report_type}")