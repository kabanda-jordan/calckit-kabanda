import math

import pytest

from calc_toolkit import (
    CalcError,
    EmptySequenceError,
    average,
    geometric_mean,
    harmonic_mean,
    maximum,
    mean,
    median,
    minimum,
    mode,
    standard_deviation,
    total,
    value_range,
    variance,
)


def test_total():
    assert total(1, 2, 3, 4) == 10.0


def test_mean_and_average():
    assert mean(2, 4, 6) == 4.0
    assert average(2, 4, 6) == 4.0
    assert mean(5) == 5.0


def test_median():
    assert median(1, 3, 2) == 2.0
    assert median(4, 1, 3, 2) == 2.5


def test_mode_picks_smallest_on_tie():
    assert mode(1, 2, 2, 3) == 2.0
    assert mode(1, 1, 2, 2) == 1.0


def test_min_max_range():
    assert minimum(3, 1, 2) == 1.0
    assert maximum(3, 1, 2) == 3.0
    assert value_range(3, 1, 2) == 2.0


def test_variance_and_stdev():
    assert variance(2, 4, 4, 4, 5, 5, 7, 9) == pytest.approx(4.0)
    assert variance(2, 4, 4, 4, 5, 5, 7, 9, sample=True) == pytest.approx(32 / 7)
    assert standard_deviation(2, 4, 4, 4, 5, 5, 7, 9) == pytest.approx(2.0)


def test_population_variance_single_value():
    assert variance(7) == 0.0
    with pytest.raises(CalcError):
        variance(7, sample=True)


def test_means():
    assert geometric_mean(1, 4) == pytest.approx(2.0)
    assert harmonic_mean(1, 4) == pytest.approx(1.6)
    with pytest.raises(CalcError):
        geometric_mean(0)
    with pytest.raises(CalcError):
        harmonic_mean(0)


def test_empty_sequence():
    with pytest.raises(EmptySequenceError):
        mean()


def test_non_numeric():
    with pytest.raises(CalcError):
        median(1, "two")