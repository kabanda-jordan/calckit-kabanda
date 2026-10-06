import pytest

from calc_toolkit import (
    CalcError,
    DivisionByZeroError,
    absolute,
    add,
    divide,
    factorial,
    integer_divide,
    modulus,
    multiply,
    power,
    square_root,
    subtract,
)


def test_add():
    assert add(1, 2, 3) == 6
    assert add(1.5, 2) == 3.5


def test_add_rejects_nothing_given():
    with pytest.raises(CalcError):
        add()


def test_subtract():
    assert subtract(10, 3) == 7
    assert subtract(10, 3, 2) == 5


def test_multiply():
    assert multiply(2, 3, 4) == 24
    assert multiply(5) == 5


def test_divide():
    assert divide(10, 4) == 2.5
    assert divide(9, 3) == 3.0


def test_divide_by_zero():
    with pytest.raises(DivisionByZeroError):
        divide(1, 0)


def test_integer_divide():
    assert integer_divide(10, 3) == 3
    assert integer_divide(-10, 3) == -4


def test_power_and_modulus():
    assert power(2, 10) == 1024
    assert modulus(10, 3) == 1
    with pytest.raises(DivisionByZeroError):
        modulus(10, 0)


def test_root_and_log():
    assert square_root(9) == 3.0
    with pytest.raises(CalcError):
        square_root(-1)


def test_absolute_and_factorial():
    assert absolute(-5) == 5
    assert factorial(5) == 120
    assert factorial(0) == 1
    with pytest.raises(CalcError):
        factorial(-1)


def test_booleans_rejected():
    with pytest.raises(CalcError):
        add(True, 1)


def test_strings_rejected():
    with pytest.raises(CalcError):
        multiply("2", 3)