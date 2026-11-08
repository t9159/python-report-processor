import random
from datetime import datetime, timedelta
from typing import Tuple


class MockEngine:
    """Utility class for generating logical mock data for reports."""

    @staticmethod
    def generate_entry_exit_times() -> Tuple[str, str, float]:
        """
        Generates a logical morning entry time and an exit time based on shift length.
        Returns: (entry_time_str, exit_time_str, total_hours_float)
        """
        # Generate entry time between 07:00 and 09:30
        start_hour = random.randint(7, 9)
        start_minute = random.choice([0, 15, 30, 45])
        entry_dt = datetime.strptime(f"{start_hour:02d}:{start_minute:02d}", "%H:%M")

        # Generate shift length (between 6 and 10 hours)
        shift_length = random.choice([6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0])
        exit_dt = entry_dt + timedelta(hours=shift_length)

        entry_str = entry_dt.strftime("%H:%M")
        exit_str = exit_dt.strftime("%H:%M")

        return entry_str, exit_str, shift_length

    @staticmethod
    def get_break_time_hours(total_hours: float) -> float:
        """Returns 0.5 (half an hour) break if shift is 6 hours or longer, else 0."""
        return 0.5 if total_hours >= 6.0 else 0.0

    @staticmethod
    @staticmethod
    def format_time_str(hours: float) -> str:
        """Convert decimal hours to a time string in HH:MM format."""
        h = int(hours)
        m = int(round((hours - h) * 60))
        return f"{h:02d}:{m:02d}"

    @staticmethod
    def calculate_overtime(net_hours: float) -> Tuple[float, float, float]:
        """
        Splits net working hours into standard (100%), 125%, and 150% rates.
        Assuming standard workday is up to 8 hours.
        Returns: (rate_100, rate_125, rate_150)
        """
        rate_100 = min(net_hours, 8.0)
        remainder = net_hours - rate_100

        rate_125 = min(remainder, 2.0) if remainder > 0 else 0.0
        remainder -= rate_125

        rate_150 = remainder if remainder > 0 else 0.0

        return rate_100, rate_125, rate_150