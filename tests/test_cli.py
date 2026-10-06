import pytest

from calc_toolkit.cli import main


def test_add(capsys):
    assert main(["add", "1", "2", "3"]) == 0
    assert capsys.readouterr().out.strip() == "6"


def test_divide_renders_without_decimal_point(capsys):
    assert main(["divide", "9", "3"]) == 0
    assert capsys.readouterr().out.strip() == "3"


def test_mean(capsys):
    assert main(["mean", "2", "4", "6"]) == 0
    assert capsys.readouterr().out.strip() == "4"


def test_divide_by_zero_returns_error(capsys):
    assert main(["divide", "1", "0"]) == 1
    assert "divide by zero" in capsys.readouterr().err


def test_unknown_operation(capsys):
    assert main(["frobnicate", "1"]) == 2


def test_non_numeric_argument(capsys):
    assert main(["add", "abc"]) == 2


def test_wrong_argument_count(capsys):
    assert main(["divide", "1", "2", "3"]) == 2


def test_missing_numbers(capsys):
    assert main(["add"]) == 2


def test_factorial(capsys):
    assert main(["factorial", "5"]) == 0
    assert capsys.readouterr().out.strip() == "120"