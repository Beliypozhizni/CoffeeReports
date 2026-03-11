import pytest

from coffee_reports import cli
from coffee_reports.io import InputError
from coffee_reports.models import Report


@pytest.fixture
def fake_report() -> Report:
    return Report(
        headers=("student", "median_coffee"),
        rows=[
            ("Bob", 40),
            ("Alice", 15),
        ],
    )


def test_build_parser_parses_required_args():
    parser = cli.build_parser()

    args = parser.parse_args(["-f", "a.csv", "b.csv", "-r", "median-coffee"])

    assert args.files == ["a.csv", "b.csv"]
    assert args.report == "median-coffee"


def test_render_report():
    rendered = cli.render_report(
        headers=("student", "median_coffee"),
        rows=[("Bob", 40), ("Alice", 15)],
    )

    assert "student" in rendered
    assert "median_coffee" in rendered
    assert "Bob" in rendered
    assert "Alice" in rendered


def test_main_success(monkeypatch, capsys, fake_report):
    class FakeBuilder:
        def build(self, rows):
            assert rows == [{"student": "Alice", "coffee_spent": "10"}]
            return fake_report

    monkeypatch.setattr(
        cli,
        "read_rows",
        lambda files: [{"student": "Alice", "coffee_spent": "10"}],
    )
    monkeypatch.setattr(cli, "get_report_builder", lambda report_name: FakeBuilder())

    exit_code = cli.main(["-f", "data.csv", "-r", "median-coffee"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "student" in captured.out
    assert "median_coffee" in captured.out
    assert captured.err == ""


def test_main_returns_2_for_input_error(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "read_rows",
        lambda files: (_ for _ in ()).throw(InputError("bad input")),
    )

    exit_code = cli.main(["-f", "data.csv", "-r", "median-coffee"])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Input error: bad input" in captured.err
    assert captured.out == ""


def test_main_returns_1_for_unexpected_error(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "read_rows",
        lambda files: [{"student": "Alice", "coffee_spent": "10"}],
    )
    monkeypatch.setattr(
        cli,
        "get_report_builder",
        lambda report_name: (_ for _ in ()).throw(RuntimeError("boom")),
    )

    exit_code = cli.main(["-f", "data.csv", "-r", "median-coffee"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: boom" in captured.err
    assert captured.out == ""


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["-f", "data.csv"],
        ["-r", "median-coffee"],
    ],
)
def test_main_exits_on_invalid_args(argv):
    with pytest.raises(SystemExit):
        cli.main(argv)
