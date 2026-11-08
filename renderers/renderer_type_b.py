from pathlib import Path
from core.models import ReportDataB
from renderers.base_renderer import BaseRenderer


class RendererTypeB(BaseRenderer):
    """Renderer for generating the visual PDF of Report Type B (Employee Card)."""

    def render(self, data: ReportDataB, output_path: str | Path) -> None:
        # Initialize canvas and layout variables using the shared base method
        pdf_canvas, width, height, y_position, right_margin = self._init_canvas(output_path)

        pdf_canvas.setFont(self.font_name, 14)

        title_text = self._rtl('כרטיס עובד לחודש')
        pdf_canvas.drawRightString(right_margin, y_position, title_text)

        y_position -= 40
        pdf_canvas.setFont(self.font_name, 10)

        summary_lines = [
            f'שם העובד: {data.employee_name}',
            f'סה"כ ימי עבודה לחודש: {data.total_monthly_days}',
            f'סה"כ שעות חודשיות: {data.total_monthly_hours}',
            f'מחיר לשעה: {data.hourly_rate}',
            f'סה"כ לתשלום: {data.total_payment}'
        ]

        for line in summary_lines:
            pdf_canvas.drawRightString(right_margin, y_position, self._rtl(line))
            y_position -= 20

        y_position -= 20

        headers = ["תאריך", "יום בשבוע", "שעת כניסה", "שעת יציאה", 'סה"כ שעות', "הערות"]
        x_offsets = [0, 60, 130, 210, 290, 360]

        for header, offset in zip(headers, x_offsets):
            pdf_canvas.drawRightString(right_margin - offset, y_position, self._rtl(header))

        y_position -= 20

        for record in data.records:
            pdf_canvas.drawRightString(right_margin - x_offsets[0], y_position, self._rtl(record.date_str))
            pdf_canvas.drawRightString(right_margin - x_offsets[1], y_position, self._rtl(record.day_of_week))
            pdf_canvas.drawRightString(right_margin - x_offsets[2], y_position, self._rtl(record.entry_time))
            pdf_canvas.drawRightString(right_margin - x_offsets[3], y_position, self._rtl(record.exit_time))
            pdf_canvas.drawRightString(right_margin - x_offsets[4], y_position, self._rtl(record.total_hours))

            notes_str = record.notes if record.notes else ""
            pdf_canvas.drawRightString(right_margin - x_offsets[5], y_position, self._rtl(notes_str))

            y_position -= 20

            y_position = self._check_page_break(pdf_canvas, y_position, height)

        pdf_canvas.save()