from coffee_reports.models import Report
from coffee_reports.reports.median_coffee import MedianCoffeeReportBuilder


def test_median_coffee_report_builder_name():
    assert MedianCoffeeReportBuilder.name() == "median-coffee"


def test_median_coffee_report_builder_build(sample_rows):
    builder = MedianCoffeeReportBuilder()

    result = builder.build(sample_rows)

    assert isinstance(result, Report)
    assert result.headers == ("student", "median_coffee")
    assert result.rows == [
        ("Bob", 40),
        ("Alice", 15),
        ("Charlie", 15),
    ]


def test_median_coffee_report_builder_single_value_per_student():
    builder = MedianCoffeeReportBuilder()

    rows = [
        {"student": "Alice", "coffee_spent": "7"},
        {"student": "Bob", "coffee_spent": "3"},
    ]

    result = builder.build(rows)

    assert result.rows == [
        ("Alice", 7),
        ("Bob", 3),
    ]
