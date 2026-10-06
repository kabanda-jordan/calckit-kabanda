"""Safe arithmetic expression evaluation.

The web calculator needs to turn a string like ``2 + 3 * sqrt(16)`` into a
number. That is deliberately *not* done with ``eval()``, because ``eval`` would
execute whatever it was given. This module implements a small recursive-descent
parser that understands only numbers, operators, parentheses and a fixed set of
functions, so nothing outside that table can run.
"""

from __future__ import annotations

import math
from typing import Callable

from .errors import CalcError
from .errors import DivisionByZeroError

OPERATORS = {"+", "-", "*", "/", "//", "%", "**", "(", ")", ","}

# Longest first, so "//" wins over "/" and "**" wins over "*".
MULTI_CHAR_OPERATORS = ("//", "**")


def _is_number_char(char: str) -> bool:
    return char.isdigit() or char == "."


def tokenize(text: str) -> list[str]:
    """Split ``text`` into number, operator, name and parenthesis tokens."""
    tokens: list[str] = []
    index = 0
    while index < len(text):
        char = text[index]

        if char.isspace():
            index += 1
        elif _is_number_char(char):
            start = index
            while index < len(text) and _is_number_char(text[index]):
                index += 1
            # Scientific notation such as 1e-9.
            if index < len(text) and text[index] in "eE":
                probe = index + 1
                if probe < len(text) and text[probe] in "+-":
                    probe += 1
                if probe < len(text) and text[probe].isdigit():
                    index = probe
                    while index < len(text) and text[index].isdigit():
                        index += 1
            tokens.append(text[start:index])
        elif char.isalpha() or char == "_":
            start = index
            while index < len(text) and (text[index].isalnum() or text[index] == "_"):
                index += 1
            tokens.append(text[start:index].lower())
        elif char in OPERATORS:
            two = text[index : index + 2]
            if two in MULTI_CHAR_OPERATORS:
                tokens.append(two)
                index += 2
            else:
                tokens.append(char)
                index += 1
        else:
            raise CalcError(f"Unexpected character {char!r} in expression")
    return tokens


class _Parser:
    """Recursive-descent parser over a token list."""

    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.position = 0

    def peek(self) -> str | None:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def take(self) -> str:
        token = self.peek()
        if token is None:
            raise CalcError("Expression ended unexpectedly")
        self.position += 1
        return token

    def parse(self) -> float:
        if not self.tokens:
            raise CalcError("Expression is empty")
        value = self.expression()
        if self.position != len(self.tokens):
            raise CalcError(f"Unexpected token {self.tokens[self.position]!r}")
        return value

    def expression(self) -> float:
        value = self.term()
        while self.peek() in ("+", "-"):
            operator = self.take()
            right = self.term()
            value = value + right if operator == "+" else value - right
        return value

    def term(self) -> float:
        value = self.factor()
        while self.peek() in ("*", "/", "//", "%"):
            operator = self.take()
            right = self.factor()
            if operator == "*":
                value *= right
            elif operator == "/":
                if right == 0:
                    raise DivisionByZeroError("Cannot divide by zero")
                value /= right
            elif operator == "//":
                if right == 0:
                    raise DivisionByZeroError("Cannot divide by zero")
                value = float(value // right)
            else:
                if right == 0:
                    raise DivisionByZeroError("Cannot take a remainder of zero")
                value = math.fmod(value, right)
        return value

    def factor(self) -> float:
        base = self.unary()
        if self.peek() == "**":
            self.take()
            # Right associative, so 2 ** 3 ** 2 means 2 ** (3 ** 2).
            return base ** self.factor()
        return base

    def unary(self) -> float:
        if self.peek() in ("+", "-"):
            operator = self.take()
            value = self.unary()
            return value if operator == "+" else -value
        return self.atom()

    def atom(self) -> float:
        token = self.peek()

        if token is None:
            raise CalcError("Expression ended unexpectedly")

        if token == "(":
            self.take()
            value = self.expression()
            if self.peek() != ")":
                raise CalcError("Missing closing parenthesis")
            self.take()
            return value

        if _is_number_char(token[0]) and token[0] != ".":
            self.take()
            try:
                return float(token)
            except ValueError:
                raise CalcError(f"Invalid number {token!r}") from None

        if token[0].isalpha() or token[0] == "_":
            name = self.take()
            if self.peek() != "(":
                raise CalcError(f"Unknown name {name!r}; functions need brackets")
            self.take()
            args = self.arguments()
            function = FUNCTIONS.get(name)
            if function is None:
                raise CalcError(f"Unknown function {name!r}")
            return float(function(*args))

        raise CalcError(f"Unexpected token {token!r}")

    def arguments(self) -> list[float]:
        args: list[float] = []
        if self.peek() == ")":
            self.take()
            return args
        while True:
            args.append(self.expression())
            token = self.take()
            if token == ")":
                return args
            if token != ",":
                raise CalcError("Expected ',' or ')' in arguments")


def _factorial(value: float) -> float:
    if value < 0 or value != int(value):
        raise CalcError("factorial() needs a whole number of 0 or more")
    return float(math.factorial(int(value)))


def _root(value: float, degree: float = 2) -> float:
    if value < 0:
        raise CalcError("root() needs a value of 0 or more")
    if degree == 0:
        raise CalcError("root() degree cannot be zero")
    return float(value ** (1 / degree))


FUNCTIONS: dict[str, Callable[..., float]] = {
    "sqrt": math.sqrt,
    "root": _root,
    "abs": abs,
    "log": lambda value, base=10: math.log(value, base),
    "ln": math.log,
    "factorial": _factorial,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": lambda value, digits=0: round(value, int(digits)),
    "exp": math.exp,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "min": min,
    "max": max,
    "pow": pow,
}


def evaluate(expression: str) -> float:
    """Evaluate an arithmetic expression and return a float.

    Args:
        expression: for example ``"2 + 3 * sqrt(16)"``.

    Raises:
        CalcError: on anything the parser does not understand.
        DivisionByZeroError: on division or remainder by zero.
    """
    if not isinstance(expression, str):
        raise CalcError("Expression must be a string")
    return _Parser(tokenize(expression)).parse()