"""Basic arithmetic operations.

Every function accepts any number of values and returns a numeric result.
Numbers can be ints or floats; ``True``/``False`` are rejected on purpose so
that booleans never sneak in as 0/1.
"""

from __future__ import annotations

import math
from typing import Iterable, Union

from .errors import CalcError, DivisionByZeroError

Number = Union[int, float]


def _validate(values: Iterable[Number], op: str) -> list:
    """Return ``values`` as a list of numbers, or raise ``CalcError``."""
    out = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise CalcError(
                f"{op}() only accepts int or float, got {type(value).__name__}: {value!r}"
            )
        out.append(value)
    if not out:
        raise CalcError(f"{op}() needs at least one value")
    return out


def _check_nonzero(divisor: Number, op: str) -> None:
    if divisor == 0:
        raise DivisionByZeroError(f"{op}() cannot divide by zero")


def add(*values: Number) -> Number:
    """Return the sum of all ``values``."""
    return sum(_validate(values, "add"))


def subtract(minuend: Number, *subtrahends: Number) -> Number:
    """Subtract every following value from ``minuend``.

    ``subtract(10, 3, 2)`` -> ``5``
    """
    _validate((minuend, *subtrahends), "subtract")
    result = minuend
    for value in subtrahends:
        result -= value
    return result


def multiply(*values: Number) -> Number:
    """Return the product of all ``values``."""
    result = 1
    for value in _validate(values, "multiply"):
        result *= value
    return result


def divide(dividend: Number, divisor: Number) -> Number:
    """Return ``dividend / divisor``.

    Raises:
        DivisionByZeroError: if ``divisor`` is zero.
    """
    _validate((dividend, divisor), "divide")
    _check_nonzero(divisor, "divide")
    return dividend / divisor


def integer_divide(dividend: Number, divisor: Number) -> int:
    """Return floor division (``//``) as an int."""
    _validate((dividend, divisor), "integer_divide")
    _check_nonzero(divisor, "integer_divide")
    return int(dividend // divisor)


def power(base: Number, exponent: Number) -> Number:
    """Return ``base ** exponent``."""
    _validate((base, exponent), "power")
    return base**exponent


def modulus(dividend: Number, divisor: Number) -> Number:
    """Return the remainder (``%``)."""
    _validate((dividend, divisor), "modulus")
    _check_nonzero(divisor, "modulus")
    return dividend % divisor


def absolute(value: Number) -> Number:
    """Return the absolute value of ``value``."""
    _validate((value,), "absolute")
    return abs(value)


def root(value: Number, degree: Number = 2) -> float:
    """Return the ``degree``-th root of a non-negative ``value``."""
    _validate((value, degree), "root")
    if value < 0:
        raise CalcError(f"root() needs a non-negative value, got {value}")
    if degree == 0:
        raise CalcError("root() degree cannot be zero")
    return float(value ** (1 / degree))


def square_root(value: Number) -> float:
    """Return the square root of ``value``."""
    return root(value, 2)


def logarithm(value: Number, base: Number = math.e) -> float:
    """Return the logarithm of ``value`` in the given ``base``."""
    _validate((value, base), "logarithm")
    if value <= 0:
        raise CalcError(f"logarithm() needs a value above zero, got {value}")
    _check_nonzero(base, "logarithm")
    return math.log(value, base)


def factorial(value: int) -> int:
    """Return ``value!`` for non-negative integers."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise CalcError(f"factorial() needs an int, got {type(value).__name__}")
    if value < 0:
        raise CalcError(f"factorial() needs a non-negative value, got {value}")
    return math.factorial(value)