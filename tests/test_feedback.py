#!/usr/bin/env python3
# Core Library modules

# Third party modules
import pytest
from colorama import Back, Fore, Style

# First party modules
from pynamer import pynamer


@pytest.mark.parametrize(
    "message, message_type, result",
    [
        ("null", "null", f"{Fore.WHITE}{Style.BRIGHT}null{Style.RESET_ALL}\n"),
        ("nominal", "nominal", f"{Fore.GREEN}{Style.BRIGHT}nominal{Style.RESET_ALL}\n"),
        (
            "warning",
            "warning",
            f"{Fore.YELLOW}{Back.BLACK}{Style.BRIGHT}warning{Style.RESET_ALL}\n",
        ),
        (
            "error",
            "error",
            f"{Fore.RED}{Back.BLACK}{Style.BRIGHT}error{Style.RESET_ALL}\n",
        ),
        ("error", "critical", ""),
    ],
)
def test_feedback(message, message_type, result, capfd):
    """Pytest test to assert mark parametrize pytest feature."""
    pynamer._feedback(message, message_type)
    captured = capfd.readouterr()
    assert captured.out == result


def test_idlemode(capfd):
    assert pynamer.config.idlemode == 0
    pynamer.config.idlemode = 1
    pynamer._feedback("warning", "warning")
    captured = capfd.readouterr()
    assert captured.out == "warning\n"
    pynamer.config.idlemode = 0
