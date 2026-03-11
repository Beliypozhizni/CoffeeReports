import argparse
import sys
from typing import Sequence

from tabulate import tabulate

from coffee_reports.io import read_rows, InputError
from coffee_reports.reports import available_reports, get_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="coffee-reports",
        description="Reads CSV files and generates reports.",
    )
    parser.add_argument(
        "-f",
        "--files",
        required=True,
        nargs="+",
        help="One or more CSV file paths",
    )
    parser.add_argument(
        "-r",
        "--report",
        required=True,
        choices=available_reports(),
        help="Report name",
    )
    return parser


def render_report(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    return tabulate(
        rows,
        headers=headers,
        tablefmt="psql",
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        rows = read_rows(args.files)
        builder = get_report(args.report)
        report = builder.build(rows)
        print(render_report(report.headers, report.rows))
        return 0
    except InputError as e:
        print(f"Input error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
