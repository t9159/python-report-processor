import random
from datetime import datetime, timedelta
from typing import List
from core.models import DailyRecordA, ReportDataA
from data_builders.base_builder import BaseBuilder


class BuilderTypeA(BaseBuilder):
    """Builder for generating mock data for Report Type A."""

    WORKPLACES = ["משרד", "שטח", "סניף מרכזי", "גליליון", "מחסן", "סניף צפון", "גונן"]

    # Hebrew day names matching the weekday() index (0 = Monday, 5 = Saturday, 6 = Sunday)
    HEBREW_DAYS = ["יום שני", "יום שלישי", "יום רביעי", "יום חמישי", "יום שישי", "שבת", "יום ראשון"]

    def build(self) -> ReportDataA:
        records: List[DailyRecordA] = []

        sum_100 = 0.0
        sum_125 = 0.0
        sum_150 = 0.0
        sum_shabbat = 0.0
        total_monthly_hours_sum = 0.0

        current_date = datetime(2026, 10, 1)
        target_days = random.randint(15, 22)
        days_generated = 0

        while days_generated < target_days and current_date.month == 10:
            if random.random() < 0.3:
                current_date += timedelta(days=1)
                continue

            workplace = random.choice(self.WORKPLACES)

            entry_hour = random.randint(7, 9)
            entry_minute = random.choice([0, 30])
            exit_hour = random.randint(15, 18)
            exit_minute = random.choice([0, 30])

            entry_decimal = entry_hour + (entry_minute / 60.0)
            exit_decimal = exit_hour + (exit_minute / 60.0)

            break_hours = 0.5
            break_str = "00:30"

            net_hours = (exit_decimal - entry_decimal) - break_hours

            if net_hours <= 0:
                current_date += timedelta(days=1)
                continue

            total_monthly_hours_sum += net_hours

            daily_100 = 0.0
            daily_125 = 0.0
            daily_150 = 0.0
            daily_shabbat = 0.0

            day_of_week_idx = current_date.weekday()
            day_name = self.HEBREW_DAYS[day_of_week_idx]

            if day_of_week_idx == 5:
                daily_shabbat = net_hours
            else:
                if net_hours > 8.0:
                    daily_100 = 8.0
                    overtime = net_hours - 8.0
                    if overtime > 2.0:
                        daily_125 = 2.0
                        daily_150 = overtime - 2.0
                    else:
                        daily_125 = overtime
                else:
                    daily_100 = net_hours

            sum_100 += daily_100
            sum_125 += daily_125
            sum_150 += daily_150
            sum_shabbat += daily_shabbat

            # Populate the record with the separated date and day fields
            record = DailyRecordA(
                date_str=current_date.strftime('%d/%m/%Y'),
                day_of_week=day_name,
                workplace=workplace,
                entry_time=f"{entry_hour:02d}:{entry_minute:02d}",
                exit_time=f"{exit_hour:02d}:{exit_minute:02d}",
                break_time=break_str,
                total_hours=f"{net_hours:.2f}",
                rate_100=f"{daily_100:.2f}" if daily_100 > 0 else "0.00",
                rate_125=f"{daily_125:.2f}" if daily_125 > 0 else "0.00",
                rate_150=f"{daily_150:.2f}" if daily_150 > 0 else "0.00",
                shabbat_150=f"{daily_shabbat:.2f}" if daily_shabbat > 0 else "0.00"
            )
            records.append(record)

            days_generated += 1
            current_date += timedelta(days=1)

        return ReportDataA(
            total_days=str(len(records)),
            total_hours_sum=f"{total_monthly_hours_sum:.2f}",
            records=records,
            total_100=f"{sum_100:.2f}",
            total_125=f"{sum_125:.2f}",
            total_150=f"{sum_150:.2f}",
            total_shabbat=f"{sum_shabbat:.2f}"
        )