"""Command line interface: ``calc <operation> <numbers...>``."""

from __future__ import annotations

import argparse
import sys

from . import __version__
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
from .errors import CalcError
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

OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "div": divide,
    "idiv": integer_divide,
    "power": power,
    "pow": power,
    "modulus": modulus,
    "mod": modulus,
    "abs": absolute,
    "root": root,
    "sqrt": square_root,
    "log": logarithm,
    "factorial": factorial,
    "total": total,
    "mean": mean,
    "average": average,
    "median": median,
    "mode": mode,
    "min": minimum,
    "max": maximum,
    "range": value_range,
    "variance": variance,
    "stdev": standard_deviation,
    "geomean": geometric_mean,
    "harmmean": harmonic_mean,
}

NEEDS_ONE = {"abs", "sqrt", "factorial"}
NEEDS_TWO = {"divide", "div", "idiv", "power", "pow", "modulus", "mod"}
ONE_OR_TWO = {"root", "log"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calckit-kabanda",
        description="Arithmetic and statistics calculator.",
        epilog="Operations: " + ", ".join(sorted(OPERATIONS)),
    )
    parser.add_argument("operation", help="e.g. add, divide, mean")
    parser.add_argument("numbers", nargs="*", help="numbers to work on")
    parser.add_argument("-V", "--version", action="version", version=f"calckit-kabanda {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    op_name = args.operation.lower()
    if op_name not in OPERATIONS:
        print(
            f"Unknown operation: {args.operation}\nOperations: " + ", ".join(sorted(OPERATIONS)),
            file=sys.stderr,
        )
        return 2

    try:
        numbers = [float(n) for n in args.numbers]
    except ValueError:
        print("All arguments must be numbers", file=sys.stderr)
        return 2

    if op_name in NEEDS_ONE and len(numbers) != 1:
        print(f"{op_name}() takes exactly 1 number", file=sys.stderr)
        return 2
    if op_name in NEEDS_TWO and len(numbers) != 2:
        print(f"{op_name}() takes exactly 2 numbers", file=sys.stderr)
        return 2
    if op_name in ONE_OR_TWO and len(numbers) > 2:
        print(f"{op_name}() takes 1 or 2 numbers", file=sys.stderr)
        return 2
    if not numbers and op_name not in NEEDS_ONE:
        print(f"{op_name}() needs at least one number", file=sys.stderr)
        return 2

    if op_name == "factorial":
        numbers = [numbers[0].is_integer() and int(numbers[0])]

    try:
        result = OPERATIONS[op_name](*numbers)
    except CalcError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if isinstance(result, float) and result.is_integer():
        print(int(result))
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())