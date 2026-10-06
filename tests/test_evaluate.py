import math

import pytest

from calc_toolkit import CalcError, DivisionByZeroError, evaluate


def test_arithmetic():
    assert evaluate("2 + 3") == 5.0
    assert evaluate("10 - 4 - 3") == 3.0
    assert evaluate("2 + 3 * 4") == 14.0
    assert evaluate("(2 + 3) * 4") == 20.0
    assert evaluate("10 / 4") == 2.5
    assert evaluate("10 // 3") == 3.0
    assert evaluate("10 % 3") == 1.0


def test_unary_and_negative():
    assert evaluate("-5") == -5.0
    assert evaluate("-5 + 8") == 3.0
    assert evaluate("3 * -2") == -6.0


def test_power_is_right_associative():
    assert evaluate("2 ** 3") == 8.0
    assert evaluate("2 ** 3 ** 2") == 512.0


def test_decimal_and_scientific_notation():
    assert evaluate("1.5 * 2") == 3.0
    assert evaluate("1e3 + 1") == 1001.0


def test_functions():
    assert evaluate("sqrt(16)") == 4.0
    assert evaluate("root(27, 3)") == 3.0
    assert evaluate("abs(-7)") == 7.0
    assert evaluate("factorial(5)") == 120.0
    # log10(1000) is 2.9999999999999996 in binary floating point.
    assert evaluate("log(1000)") == pytest.approx(3.0)
    assert evaluate("log(8, 2)") == 3.0
    assert evaluate("round(3.14159, 2)") == 3.14
    assert evaluate("max(3, 9, 2)") == 9.0
    assert evaluate("pow(3, 4)") == 81.0


def test_nested_calls():
    assert evaluate("sqrt(9) + sqrt(16)") == 7.0
    assert evaluate("2 * sqrt(3 + 6)") == 6.0
    assert evaluate("abs(-3) ** 2") == 9.0


def test_division_by_zero():
    with pytest.raises(DivisionByZeroError):
        evaluate("1 / 0")
    with pytest.raises(DivisionByZeroError):
        evaluate("1 // 0")
    with pytest.raises(DivisionByZeroError):
        evaluate("1 % 0")


def test_syntax_errors():
    for bad in ["", "2 +", "(2 + 3", "2 + 3)", "* 3", "2 $ 3", "sqrt(16"]:
        with pytest.raises(CalcError):
            evaluate(bad)


def test_unknown_names_are_rejected():
    with pytest.raises(CalcError):
        evaluate("nope(2)")
    with pytest.raises(CalcError):
        evaluate("nope")


def test_code_execution_is_impossible():
    # These would run arbitrary code if the parser used eval().
    for hostile in [
        "__import__('os').system('echo hi')",
        "().__class__.__bases__",
        "open('C:/Windows/System32/drivers/etc/hosts').read()",
        "1; import os",
        "lambda: 1",
        "[x for x in range(3)]",
        "{'a': 1}",
        "1 if 1 else 2",
    ]:
        with pytest.raises(CalcError):
            evaluate(hostile)


def test_non_string_input():
    with pytest.raises(CalcError):
        evaluate(123)


def test_large_factorial_is_sane():
    assert evaluate("factorial(0)") == 1.0
    assert math.isclose(evaluate("factorial(6)"), 720.0)