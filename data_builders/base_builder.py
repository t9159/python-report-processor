from abc import ABC, abstractmethod
from core.models import ReportDataA, ReportDataB

class BaseBuilder(ABC):
    """Abstract base class defining the strict contract for all data builders."""

    @abstractmethod
    def build(self) -> ReportDataA | ReportDataB:
        """
        Generates and returns the specific report data object.
        Must be implemented by all child builders.
        """
        pass