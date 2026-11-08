from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class ReportType(Enum):
    """Defines the types of reports the system can detect and generate."""
    WORKPLACE_A = "workplace_a"
    WORKPLACE_B = "workplace_b"
    UNKNOWN = "unknown"

# ==========================================
# Data Models for Report Type A
# ==========================================

@dataclass(frozen=True)
class DailyRecordA:
    """Represents a single row in the table of Report Type A."""
    date_str: str
    day_of_week: str
    workplace: str
    entry_time: str
    exit_time: str
    break_time: str
    total_hours: str
    rate_100: str
    rate_125: str
    rate_150: str
    shabbat_150: str

@dataclass(frozen=True)
class ReportDataA:
    """Holds all necessary data to generate a new Report Type A."""
    records: List[DailyRecordA]
    total_days: str
    total_hours_sum: str
    total_100: str = "0.0"
    total_125: str = "0.0"
    total_150: str = "0.0"
    total_shabbat: str = "0.0"


# ==========================================
# Data Models for Report Type B
# ==========================================

@dataclass(frozen=True)
class DailyRecordB:
    """Represents a single row in the table of Report Type B."""
    date_str: str
    day_of_week: str
    entry_time: str
    exit_time: str
    total_hours: str
    notes: Optional[str]

@dataclass(frozen=True)
class ReportDataB:
    """Holds all necessary data to generate a new Report Type B."""
    employee_name: str
    records: List[DailyRecordB]
    total_monthly_days: str
    total_monthly_hours: str
    hourly_rate: str
    total_payment: str