from pathlib import Path

import pytest

from coffee_reports.io import InputError, read_rows


def test_read_rows_reads_single_file(csv_file_factory):
    path = csv_file_factory(
        "students.csv",
        headers=["student", "coffee_spent"],
        rows=[
            ["Alice", "10"],
            ["Bob", "20"],
        ],
    )

    result = read_rows([str(path)])

    assert result == [
        {"student": "Alice", "coffee_spent": "10"},
        {"student": "Bob", "coffee_spent": "20"},
    ]


def test_read_rows_reads_multiple_files(csv_file_factory):
    path1 = csv_file_factory(
        "part1.csv",
        headers=["student", "coffee_spent"],
        rows=[["Alice", "10"]],
    )
    path2 = csv_file_factory(
        "part2.csv",
        headers=["student", "coffee_spent"],
        rows=[["Bob", "20"]],
    )

    result = read_rows([str(path1), str(path2)])

    assert result == [
        {"student": "Alice", "coffee_spent": "10"},
        {"student": "Bob", "coffee_spent": "20"},
    ]


@pytest.mark.parametrize(
    ("path_factory", "expected_message"),
    [
        (
            lambda tmp_path: tmp_path / "missing.csv",
            "File not found:",
        ),
        (
            lambda tmp_path: tmp_path,
            "Not a file:",
        ),
    ],
)
def test_read_rows_invalid_path_cases(
    tmp_path: Path, path_factory, expected_message: str
):
    path = path_factory(tmp_path)

    with pytest.raises(InputError, match=expected_message):
        read_rows([str(path)])


def test_read_rows_raises_for_empty_csv(tmp_path: Path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    with pytest.raises(InputError, match="Empty CSV or missing header row:"):
        read_rows([str(path)])


def test_read_rows_raises_for_malformed_row(tmp_path: Path):
    path = tmp_path / "bad.csv"
    path.write_text(
        "student,coffee_spent\n" "Alice,10\n" "Bob,20,EXTRA\n",
        encoding="utf-8",
    )

    with pytest.raises(InputError, match="Malformed CSV row in"):
        read_rows([str(path)])
