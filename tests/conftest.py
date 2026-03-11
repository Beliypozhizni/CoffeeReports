import csv
from pathlib import Path

import pytest


@pytest.fixture
def csv_file_factory(tmp_path: Path):
    def _make(name: str, headers: list[str], rows: list[list[str]]) -> Path:
        path = tmp_path / name
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return path

    return _make


@pytest.fixture
def sample_rows() -> list[dict[str, str]]:
    return [
        {"student": "Alice", "coffee_spent": "10"},
        {"student": "Bob", "coffee_spent": "30"},
        {"student": "Alice", "coffee_spent": "20"},
        {"student": "Bob", "coffee_spent": "50"},
        {"student": "Charlie", "coffee_spent": "15"},
    ]
