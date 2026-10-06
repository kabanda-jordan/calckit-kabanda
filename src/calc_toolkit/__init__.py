"""calc_toolkit - arithmetic and statistics helpers.

Examples:
    >>> from calc_toolkit import add, divide, mean
    >>> add(1, 2, 3)
    6
    >>> divide(10, 4)
    2.5
    >>> mean(2, 4, 6)
    4.0
"""

from .arithmetic import (
    absolute,
    add,
    divide,
    factorial,
    integer_divide,
    logarithm,
    modulus,
    multiply,
    power,
    root,
    square_root,
    subtract,
)
from .errors import CalcError, DivisionByZeroError, EmptySequenceError
from .evaluate import evaluate
from .statistics import (
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

__version__ = "0.3.0"

__all__ = [
    # arithmetic
    "add",
    "subtract",
    "multiply",
    "divide",
    "integer_divide",
    "power",
    "modulus",
    "absolute",
    "root",
    "square_root",
    "logarithm",
    "factorial",
    # expressions
    "evaluate",
    # statistics
    "total",
    "mean",
    "average",
    "median",
    "mode",
    "minimum",
    "maximum",
    "value_range",
    "variance",
    "standard_deviation",
    "geometric_mean",
    "harmonic_mean",
    # errors
    "CalcError",
    "DivisionByZeroError",
    "EmptySequenceError",
    "__version__",
]