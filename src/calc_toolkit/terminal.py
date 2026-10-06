"""An interactive terminal calculator for calckit-kabanda.

Launched with the ``calc-kabanda`` command. Presents a text menu covering
arithmetic, statistics and expressions, all running in your terminal with no
extra dependencies.
"""

from __future__ import annotations

import os
import sys
from typing import Callable

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


def _supports_colour() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    return True


COLOUR = _supports_colour()


def _c(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if COLOUR else text


BOLD = lambda t: _c(t, "1")  # noqa: E731
DIM = lambda t: _c(t, "2")  # noqa: E731
ACCENT = lambda t: _c(t, "38;5;214")  # noqa: E731
GOOD = lambda t: _c(t, "38;5;114")  # noqa: E731
BAD = lambda t: _c(t, "38;5;203")  # noqa: E731


def clear() -> None:
    print("\033[2J\033[H" if COLOUR else "\n" * 3)


# (label, function, how many numbers to ask for, hint)
ARITHMETIC: list[tuple[str, Callable, int, str]] = [
    ("Addition", add, 2, "a + b"),
    ("Subtraction", subtract, 2, "a - b"),
    ("Multiplication", multiply, 2, "a * b"),
    ("Division", divide, 2, "a / b"),
    ("Integer division", integer_divide, 2, "a // b"),
    ("Power", power, 2, "a ** b"),
    ("Remainder", modulus, 2, "a % b"),
    ("Absolute value", absolute, 1, "abs(a)"),
    ("Square root", square_root, 1, "sqrt(a)"),
    ("Nth root", root, 2, "root(a, n)"),
    ("Logarithm", logarithm, 2, "log(a, base)"),
    ("Factorial", lambda value: factorial(int(value)), 1, "a!"),
    ("Add many numbers", lambda *v: sum(v), 0, "sum of all entered"),
]

STATISTICS: list[tuple[str, Callable, str]] = [
    ("Sum", total, "2, 4, 6"),
    ("Mean (average)", mean, "2, 4, 6"),
    ("Median", median, "4, 1, 3, 2"),
    ("Mode", mode, "1, 2, 2, 3"),
    ("Smallest", minimum, "3, 1, 2"),
    ("Largest", maximum, "3, 1, 2"),
    ("Range", value_range, "3, 1, 2"),
    ("Variance", variance, "2, 4, 6"),
    ("Standard deviation", standard_deviation, "2, 4, 6"),
    ("Geometric mean", geometric_mean, "1, 4, 16"),
    ("Harmonic mean", harmonic_mean, "1, 4, 16"),
]


def _prompt(text: str) -> str:
    return input(text)


def _read_number(label: str) -> float:
    while True:
        raw = _prompt(f"  {label}: ").strip()
        try:
            return float(raw)
        except ValueError:
            print(BAD("  Enter a number, for example 12 or 4.5"))


def _read_numbers(label: str) -> list[float]:
    while True:
        raw = _prompt(f"  {label} (comma separated): ").strip()
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        try:
            numbers = [float(p) for p in parts]
        except ValueError:
            print(BAD("  Those are not all numbers. Try: 2, 4, 6"))
            continue
        if not numbers:
            print(BAD("  Enter at least one number."))
            continue
        return numbers


def _pause() -> None:
    """Wait for Enter so a result stays on screen before the menu redraws."""
    _prompt("  Press Enter to continue... ")


def _show(value: float) -> None:
    text = str(int(value)) if float(value).is_integer() else str(round(float(value), 10))
    print()
    print("  " + BOLD("= ") + GOOD(text))
    print()
    _pause()


def _show_error(message: str) -> None:
    print()
    print("  " + BAD(message))
    print()
    _pause()


def header() -> None:
    print()
    print("  " + BOLD("calc-kabanda") + DIM(f"  v{__version__}"))
    print("  " + DIM("Interactive terminal calculator. Type 0 or q to go back."))
    print()


def menu(title: str, entries: list[str], footer: str = "") -> str:
    print("  " + BOLD(title))
    print()
    width = len(str(len(entries)))
    for index, entry in enumerate(entries, start=1):
        print(f"  {ACCENT(str(index).rjust(width))}. {entry}")
    if footer:
        print()
        print("  " + DIM(footer))
    print()
    while True:
        choice = _prompt("  Choose: ").strip().lower()
        if choice in ("q", "quit", "exit", "0", ""):
            return ""
        if choice.isdigit() and 1 <= int(choice) <= len(entries):
            return choice
        print(BAD("  Pick a number from the list."))


def run_arithmetic() -> None:
    entries = [f"{label}  {DIM(hint)}" for label, _, _, hint in ARITHMETIC]
    while True:
        clear()
        header()
        choice = menu("Arithmetic", entries)
        if not choice:
            return
        label, function, count, _ = ARITHMETIC[int(choice) - 1]

        print()
        print("  " + BOLD(label))
        try:
            if count == 0:
                numbers = _read_numbers("Numbers")
            else:
                numbers = [
                    _read_number("First number" if i == 0 else "Second number")
                    for i in range(count)
                ]
            _show(function(*numbers))
        except CalcError as exc:
            _show_error(str(exc))


def run_statistics() -> None:
    entries = [f"{label}  {DIM('e.g. ' + hint)}" for label, _, hint in STATISTICS]
    while True:
        clear()
        header()
        choice = menu("Statistics", entries)
        if not choice:
            return
        label, function, _ = STATISTICS[int(choice) - 1]

        print()
        print("  " + BOLD(label))
        try:
            _show(function(*_read_numbers("Numbers")))
        except CalcError as exc:
            _show_error(str(exc))


def run_expressions() -> None:
    print("  Type expressions such as:")
    print("    " + ACCENT("2 + 3 * sqrt(16)"))
    print("    " + ACCENT("(10 + 5) / 3"))
    print("    " + ACCENT("factorial(5) + 1"))
    print()
    print("  " + DIM("Available functions: "))
    print("  " + DIM("sqrt, root, abs, factorial, log, ln, floor, ceil, round,"))
    print("  " + DIM("exp, sin, cos, tan, min, max, pow"))
    print()

    while True:
        expression = _prompt("  > ").strip()
        if expression.lower() in ("q", "quit", "exit", "0", ""):
            return
        try:
            _show(evaluate(expression))
        except CalcError as exc:
            _show_error(str(exc))


def run_about() -> None:
    print("  " + BOLD("calckit-kabanda") + f"  v{__version__}")
    print()
    print("  Arithmetic, statistics and expressions in your terminal.")
    print("  MIT licensed.")
    print()
    print("  " + DIM("https://pypi.org/project/calckit-kabanda/"))
    print("  " + DIM("https://github.com/kabanda-jordan/calckit-kabanda"))
    print()
    _pause()


MAIN_ENTRIES = [
    "Arithmetic        add, subtract, multiply, divide, ...",
    "Statistics        mean, median, mode, variance, ...",
    "Expressions       type free-form maths, e.g. 2 + 3 * sqrt(16)",
    "About             version and links",
]


def main() -> int:
    handlers: dict[str, Callable[[], None]] = {
        "1": run_arithmetic,
        "2": run_statistics,
        "3": run_expressions,
        "4": run_about,
    }
    try:
        while True:
            clear()
            header()
            choice = menu("Main menu", MAIN_ENTRIES, "0 or q to quit")
            if not choice:
                return 0
            handlers[choice]()
    except (KeyboardInterrupt, EOFError):
        print()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())