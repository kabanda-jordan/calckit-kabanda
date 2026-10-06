"""Tests for the interactive terminal interface.

Prompts are driven by monkeypatched input so no real TTY is needed. Each test
lists the answers in the exact order the interface asks for them.
"""

import builtins

import pytest

from calc_toolkit import terminal

# Flow for an arithmetic calculation:
#   main menu -> Arithmetic submenu -> two numbers -> pause -> submenu quit
ENTER = ""


@pytest.fixture()
def answers(monkeypatch):
    """Feed a scripted list of answers to input(), one per prompt."""
    queue: list[str] = []

    def fake_input(prompt=""):
        if not queue:
            raise AssertionError(f"unexpected prompt: {prompt!r}")
        return queue.pop(0)

    monkeypatch.setattr(builtins, "input", fake_input)
    return queue


def test_arithmetic_menu_computes_and_returns(answers, capsys):
    answers.extend(["1", "1", "2", "3", ENTER, "q", "0"])
    assert terminal.main() == 0
    out = capsys.readouterr().out
    assert "Arithmetic" in out
    assert "Addition" in out
    assert "5" in out


def test_statistics_menu(answers, capsys):
    answers.extend(["2", "2", "2, 4, 6", ENTER, "q", "0"])
    assert terminal.main() == 0
    out = capsys.readouterr().out
    assert "Mean" in out
    assert "4" in out


def test_expression_menu(answers, capsys):
    answers.extend(["3", "2 + 3 * sqrt(16)", ENTER, "q", "0"])
    assert terminal.main() == 0
    assert "14" in capsys.readouterr().out


def test_bad_number_is_retried(answers, capsys):
    # main -> arithmetic -> addition -> "abc" rejected -> 4 + 5
    answers.extend(["1", "1", "abc", "4", "5", ENTER, "q", "0"])
    terminal.main()
    out = capsys.readouterr().out
    assert "Enter a number" in out
    assert "9" in out


def test_bad_expression_is_retried(answers, capsys):
    answers.extend(["3", "2 +", ENTER, "2 + 2", ENTER, "q", "0"])
    terminal.main()
    out = capsys.readouterr().out
    assert "4" in out


def test_division_by_zero_shows_error(answers, capsys):
    # Arithmetic menu, entry 4 is Division.
    answers.extend(["1", "4", "1", "0", ENTER, "q", "0"])
    terminal.main()
    assert "divide by zero" in capsys.readouterr().out


def test_factorial_asks_for_one_number(answers, capsys):
    answers.extend(["1", "12", "5", ENTER, "q", "0"])
    terminal.main()
    assert "120" in capsys.readouterr().out


def test_add_many_asks_for_a_list(answers, capsys):
    # Arithmetic menu, last entry is "Add many numbers".
    answers.extend(["1", str(len(terminal.ARITHMETIC)), "1, 2, 3, 4", ENTER, "q", "0"])
    terminal.main()
    assert "10" in capsys.readouterr().out


def test_invalid_menu_choice_is_retried(answers, capsys):
    answers.extend(["99", "0"])
    assert terminal.main() == 0
    assert "Pick a number" in capsys.readouterr().out


def test_about_menu(answers, capsys):
    answers.extend(["4", ENTER, "0"])
    terminal.main()
    assert "pypi.org/project/calckit-kabanda" in capsys.readouterr().out


def test_quit_immediately(answers, capsys):
    answers.append("0")
    assert terminal.main() == 0
    assert "Main menu" in capsys.readouterr().out


def test_keyboard_interrupt_exits_cleanly(answers, capsys):
    def boom(prompt=""):
        raise KeyboardInterrupt

    answers.clear()
    import builtins as b

    original = b.input
    b.input = boom
    try:
        assert terminal.main() == 0
    finally:
        b.input = original


def test_eof_exits_cleanly(answers):
    # Empty queue makes input() raise AssertionError, so simulate real EOF.
    import builtins as b

    def eof(prompt=""):
        raise EOFError

    original = b.input
    b.input = eof
    try:
        assert terminal.main() == 0
    finally:
        b.input = original


def test_colour_helpers_are_plain_when_disabled():
    original = terminal.COLOUR
    try:
        terminal.COLOUR = False
        assert terminal.BOLD("x") == "x"
        assert terminal.ACCENT("y") == "y"
        assert terminal.BAD("z") == "z"
    finally:
        terminal.COLOUR = original


def test_menus_cover_the_expected_operations():
    assert len(terminal.ARITHMETIC) >= 12
    assert len(terminal.STATISTICS) >= 10
    labels = [label for label, _, _ in terminal.STATISTICS]
    for expected in ["Mean (average)", "Median", "Mode", "Standard deviation"]:
        assert expected in labels