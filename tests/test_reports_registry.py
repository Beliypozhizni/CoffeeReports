import pytest

from coffee_reports.reports import available_reports, get_report_builder
from coffee_reports.reports.median_coffee import MedianCoffeeReportBuilder


def test_available_reports():
    assert available_reports() == ["median-coffee"]


def test_get_report_builder_returns_expected_builder():
    builder = get_report_builder("median-coffee")

    assert isinstance(builder, MedianCoffeeReportBuilder)


@pytest.mark.parametrize("report_name", ["unknown", "", "median", "MEDIAN-COFFEE"])
def test_get_report_builder_raises_for_unknown_report(report_name: str):
    with pytest.raises(ValueError, match="Unknown report:"):
        get_report_builder(report_name)
