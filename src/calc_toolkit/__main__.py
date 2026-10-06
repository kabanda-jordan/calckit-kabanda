"""Entry point for ``python -m calc_toolkit``.

With arguments it runs the one-shot command line calculator; with no arguments
it opens the interactive terminal menu.
"""

from .cli import main as cli_main
from .terminal import main as terminal_main

if __import__("sys").argv[1:]:
    raise SystemExit(cli_main())
raise SystemExit(terminal_main())