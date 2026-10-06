"""Custom exceptions for calc_toolkit."""


class CalcError(Exception):
    """Base class for every error raised by calc_toolkit."""


class DivisionByZeroError(CalcError):
    """Raised when a division would divide by zero."""


class EmptySequenceError(CalcError):
    """Raised when a statistic is requested on an empty sequence."""