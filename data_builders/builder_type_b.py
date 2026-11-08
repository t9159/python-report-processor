import random
from datetime import datetime, timedelta
from typing import List
from core.models import DailyRecordB, ReportDataB
from data_builders.base_builder import BaseBuilder
from utils.mock_engine import MockEngine


class BuilderTypeB(BaseBuilder):
    """Builder for generating mock data for Report Type B (Employee Card)."""

    # Separate lists for first and last names to create diverse combinations
    FIRST_NAMES = ["אברהם", "יצחק", "יעקב", "דוד", "שלמה", "משה", "אהרן", "יוסף", "חיים", "שמעון"]
    LAST_NAMES = ["כהן", "לוי", "מזרחי", "פרידמן", "ישראלי", "אזולאי", "ביטון", "שפירא", "גולן", "קאפח"]

    def generate_random_name(self) -> str:
        """Generates a random combination of first and last name."""
        first = random.choice(self.FIRST_NAMES)
        last = random.choice(self.LAST_NAMES)
        return f"{first} {last}"

    def get_hebrew_weekday(self, dt: datetime) -> str:
        """Translates the computer's weekday (0-6) to the Hebrew weekday name."""
        days = ["שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת", "ראשון"]
        return days[dt.weekday()]

    def build(self) -> ReportDataB:
        records: List[DailyRecordB] = []
        total_monthly_hours_sum = 0.0
        work_days_count = 0

        # Pick a random employee name combination
        employee_name = self.generate_random_name()

        # Generate a random hourly rate between 30 and 45
        hourly_rate = round(random.uniform(30.0, 45.0), 2)

        # Choose a random year and month, starting the date on the 1st of the month
        year = random.choice([22, 23])
        month = random.randint(1, 12)
        current_date = datetime.strptime(f"1/{month}/{year}", "%d/%m/%y")

        # Generate 30 days of records sequentially
        for _ in range(30):
            day_name = self.get_hebrew_weekday(current_date)
            date_str = current_date.strftime("%d/%m/%y")

            # Determine if it's a day off (Saturdays or a low probability random day off)
            is_day_off = (day_name == "שבת") or (random.random() < 0.1)

            if is_day_off:
                # Create an empty record for days off
                notes = "ערב חג" if (random.random() < 0.1 and day_name != "שבת") else None
                record = DailyRecordB(
                    date_str=date_str,
                    day_of_week=day_name,
                    entry_time="",
                    exit_time="",
                    total_hours="",
                    notes=notes
                )
            else:
                # Regular work day
                work_days_count += 1
                entry_str, exit_str, total_hours = MockEngine.generate_entry_exit_times()
                total_monthly_hours_sum += total_hours

                record = DailyRecordB(
                    date_str=date_str,
                    day_of_week=day_name,
                    entry_time=entry_str,
                    exit_time=exit_str,
                    total_hours=MockEngine.format_time_str(total_hours),
                    notes=None
                )

            records.append(record)

            # Advance the date by one day
            current_date += timedelta(days=1)

        # Calculate total monthly payment
        total_payment = total_monthly_hours_sum * hourly_rate

        return ReportDataB(
            employee_name=employee_name,
            records=records,
            total_monthly_days=str(work_days_count),
            total_monthly_hours=MockEngine.format_time_str(total_monthly_hours_sum),
            hourly_rate=f"₪{hourly_rate:.2f}",
            total_payment=f"₪{total_payment:,.2f}"
        )