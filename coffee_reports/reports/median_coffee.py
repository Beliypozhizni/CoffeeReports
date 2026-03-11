from coffee_reports.models import Report
from coffee_reports.reports import ReportBuilder
from statistics import median

FIELD_STUDENT = "student"
FIELD_COFFEE_SPENT = "coffee_spent"
FIELD_MEDIAN_COFFEE = "median_coffee"


class MedianCoffeeReportBuilder(ReportBuilder):

    @classmethod
    def name(cls) -> str:
        return "median-coffee"

    def build(self, rows: list[dict[str, str]]) -> Report:
        agg: dict[str, list[int]] = {}

        for r in rows:
            student = r[FIELD_STUDENT]
            spent = int(r[FIELD_COFFEE_SPENT])

            total_spent = agg.get(student, [])
            total_spent.append(spent)

            agg[student] = total_spent

        result_rows = [(student, median(spent)) for student, spent in agg.items()]
        result_rows.sort(key=lambda x: x[1], reverse=True)

        return Report(headers=(FIELD_STUDENT, FIELD_MEDIAN_COFFEE), rows=result_rows)
