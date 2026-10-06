"""Statistics over a sequence of numbers."""

from __future__ import annotations

import math
from collections import Counter
from typing import Iterable, Union

from .errors import CalcError, EmptySequenceError

Number = Union[int, float]


def _clean(values: Iterable[Number], op: str) -> list[float]:
    """Return ``values`` as a non-empty list of floats."""
    out = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise CalcError(
                f"{op}() only accepts int or float, got {type(value).__name__}: {value!r}"
            )
        out.append(float(value))
    if not out:
        raise EmptySequenceError(f"{op}() needs at least one value")
    return out


def total(*values: Number) -> float:
    """Return the sum of all ``values``."""
    return float(sum(_clean(values, "total")))


def mean(*values: Number) -> float:
    """Return the arithmetic mean (average) of ``values``.

    Also available as ``average``.
    """
    nums = _clean(values, "mean")
    return sum(nums) / len(nums)


average = mean


def median(*values: Number) -> float:
    """Return the middle value (or mean of the two middles)."""
    nums = sorted(_clean(values, "median"))
    mid = len(nums) // 2
    if len(nums) % 2:
        return nums[mid]
    return (nums[mid - 1] + nums[mid]) / 2


def mode(*values: Number) -> float:
    """Return the most common value.

    With several tied values the smallest one is returned.
    """
    counts = Counter(_clean(values, "mode"))
    top = max(counts.values())
    return min(value for value, count in counts.items() if count == top)


def minimum(*values: Number) -> float:
    """Return the smallest value."""
    return min(_clean(values, "minimum"))


def maximum(*values: Number) -> float:
    """Return the largest value."""
    return max(_clean(values, "maximum"))


def value_range(*values: Number) -> float:
    """Return ``max - min``."""
    nums = _clean(values, "value_range")
    return max(nums) - min(nums)


def variance(*values: Number, sample: bool = False) -> float:
    """Return the variance.

    Args:
        sample: use n-1 (Bessel's correction) instead of n.
    """
    nums = _clean(values, "variance")
    if sample and len(nums) < 2:
        raise CalcError("variance() with sample=True needs at least two values")
    avg = sum(nums) / len(nums)
    divisor = len(nums) - 1 if sample else len(nums)
    return sum((n - avg) ** 2 for n in nums) / divisor


def standard_deviation(*values: Number, sample: bool = False) -> float:
    """Return the standard deviation (square root of the variance)."""
    return math.sqrt(variance(*values, sample=sample))


def geometric_mean(*values: Number) -> float:
    """Return the geometric mean. All values must be positive."""
    nums = _clean(values, "geometric_mean")
    if any(n <= 0 for n in nums):
        raise CalcError("geometric_mean() only accepts values above zero")
    return math.exp(sum(math.log(n) for n in nums) / len(nums))


def harmonic_mean(*values: Number) -> float:
    """Return the harmonic mean. All values must be non-zero."""
    nums = _clean(values, "harmonic_mean")
    if any(n == 0 for n in nums):
        raise CalcError("harmonic_mean() cannot accept zero")
    return len(nums) / sum(1 / n for n in nums)