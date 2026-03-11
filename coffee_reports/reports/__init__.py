from coffee_reports.reports.base import ReportBuilder
from coffee_reports.reports.median_coffee import MedianCoffeeReportBuilder

_REPORTS: dict[str, ReportBuilder] = {
    MedianCoffeeReportBuilder.name(): MedianCoffeeReportBuilder(),
}


def available_reports() -> list[str]:
    return sorted(_REPORTS.keys())


def get_report_builder(report_name: str) -> ReportBuilder:
    try:
        return _REPORTS[report_name]
    except KeyError:
        raise ValueError(
            f"Unknown report: {report_name!r}. Available: {', '.join(available_reports())}"
        )
