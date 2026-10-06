# calckit-kabanda

Arithmetic and statistics helpers for Python, plus a `calckit-kabanda` command line tool.

## Terminal interface

`calc-kabanda` opens an interactive menu in your terminal:

```powershell
calc-kabanda
```

```
  calc-kabanda  v0.3.0
  Interactive terminal calculator. Type 0 or q to go back.

  Main menu

  1. Arithmetic        add, subtract, multiply, divide, ...
  2. Statistics        mean, median, mode, variance, ...
  3. Expressions       type free-form maths, e.g. 2 + 3 * sqrt(16)
  4. About             version and links
```

Arithmetic has 13 entries (addition through factorial, plus adding many numbers
at once). Statistics has 11 (sum, mean, median, mode, min, max, range,
variance, standard deviation, geometric mean, harmonic mean). Each menu asks for
the numbers it needs and shows the result until you press Enter.

Expression mode accepts `+ - * / // % **`, parentheses, and functions: `sqrt`,
`root`, `abs`, `factorial`, `log`, `ln`, `floor`, `ceil`, `round`, `exp`, `sin`,
`cos`, `tan`, `min`, `max`, `pow`.

```
  > 2 + 3 * sqrt(16)
  = 14
```

Expressions are parsed by a hand-written recursive-descent parser, never
`eval()`, so nothing outside that list can run. Entering
`__import__('os').system('...')` returns an error instead of executing.

Ctrl+C or `q` at any prompt backs out. No dependencies beyond the standard
library.

If the command is not found on your machine, `python -m calc_toolkit` opens the
same menu, and `python -m calc_toolkit add 1 2 3` runs the one-shot form.

## Install

From GitHub (no PyPI account needed, works immediately):

```powershell
pip install git+https://github.com/kabanda-jordan/calckit-kabanda.git
```

From PyPI, once published:

```powershell
pip install calckit-kabanda
```

Or from a checkout:

```powershell
pip install -e .
```

The distribution is named `calckit-kabanda` on PyPI, but the import name stays
`calc_toolkit`, so code reads:

```python
from calc_toolkit import add, subtract, multiply, divide, mean, median
```

## Library use

```python
add(1, 2, 3)            # 6
subtract(10, 3, 2)      # 5
multiply(2, 3, 4)       # 24
divide(10, 4)           # 2.5

mean(2, 4, 6)           # 4.0  (same as average)
median(1, 3, 2)         # 2.0
mode(1, 2, 2, 3)        # 2.0
```

### Expressions

`evaluate` parses a string safely, with no use of `eval`:

```python
from calc_toolkit import evaluate

evaluate("2 + 3 * sqrt(16)")   # 14.0
evaluate("(10 + 5) / 3")        # 5.0
evaluate("2 ** 3 ** 2")         # 512.0  (right associative)
evaluate("factorial(5) + 1")    # 121.0
```

### Arithmetic

| Function | Example | Result |
| --- | --- | --- |
| `add(*values)` | `add(1, 2, 3)` | `6` |
| `subtract(a, *rest)` | `subtract(10, 3)` | `7` |
| `multiply(*values)` | `multiply(2, 3, 4)` | `24` |
| `divide(a, b)` | `divide(10, 4)` | `2.5` |
| `integer_divide(a, b)` | `integer_divide(10, 3)` | `3` |
| `power(base, exp)` | `power(2, 10)` | `1024` |
| `modulus(a, b)` | `modulus(10, 3)` | `1` |
| `absolute(x)` | `absolute(-5)` | `5` |
| `root(x, degree=2)` | `root(27, 3)` | `3.0` |
| `square_root(x)` | `square_root(9)` | `3.0` |
| `logarithm(x, base=e)` | `logarithm(8, 2)` | `3.0` |
| `factorial(n)` | `factorial(5)` | `120` |

### Statistics

All statistics accept a variable number of values, so both
`mean([2, 4, 6])` and `mean(2, 4, 6)` work.

| Function | Example | Result |
| --- | --- | --- |
| `total(*values)` | `total(1, 2, 3)` | `6.0` |
| `mean(*values)` / `average` | `mean(2, 4, 6)` | `4.0` |
| `median(*values)` | `median(4, 1, 3, 2)` | `2.5` |
| `mode(*values)` | `mode(1, 2, 2)` | `2.0` |
| `minimum(*values)` | `min(3, 1, 2)` | `1.0` |
| `maximum(*values)` | `max(3, 1, 2)` | `3.0` |
| `value_range(*values)` | `range(3, 1, 2)` | `2.0` |
| `variance(*values, sample=False)` | `variance(2, 4, 6)` | `2.666…` |
| `standard_deviation(*values)` | `stdev(2, 4, 6)` | `1.632…` |
| `geometric_mean(*values)` | `geometric_mean(1, 4)` | `2.0` |
| `harmonic_mean(*values)` | `harmonic_mean(1, 4)` | `1.6` |

### Errors

Everything raises `CalcError` (a plain `Exception` subclass):

- `DivisionByZeroError` for `divide(1, 0)`, `modulus(1, 0)`, `integer_divide(1, 0)`
- `EmptySequenceError` for `mean()` with no values
- `CalcError` for bad types (strings, booleans, negatives under a root, and so on)

Booleans are rejected on purpose, so `add(True, 1)` fails instead of silently
treating `True` as `1`.

## Command line

```powershell
calckit-kabanda add 1 2 3
calckit-kabanda divide 10 4
calckit-kabanda mean 2 4 6
calckit-kabanda median 4 1 3 2
calckit-kabanda sqrt 9
calckit-kabanda factorial 5
calckit-kabanda --help
```

Without installing the script, use the module form:

```powershell
python -m calc_toolkit add 1 2 3
```

Exit codes: `0` success, `1` calculation error, `2` bad arguments.

## Tests

```powershell
pytest
```