#!/usr/bin/env python3
"""Tests for CLI scripts"""

# Core Library modules

# Third party modules
from click.testing import CliRunner

# First party modules
from pynamer import pynamer_cli


def test_author() -> None:
    """Test function to assert correct author name."""
    runner = CliRunner()
    result = runner.invoke(pynamer_cli.author)
    print(result.output)
    assert result.exit_code == 0
    assert result.output == "Author name: Stephen R A King\n"


def test_author_verbose() -> None:
    """Test function to assert correct verbose author name."""
    runner = CliRunner()
    result = runner.invoke(pynamer_cli.author, ["--verbose"])
    print(result.output)
    assert result.exit_code == 0
    assert (
        result.output == "Author name: Stephen R A King\n"
        "Author eMail: sking.github@gmail.com\n"
    )


def test_author_help() -> None:
    """Test function to assert correct author help text."""
    runner = CliRunner()
    result = runner.invoke(pynamer_cli.author, ["--help"])
    print(result.output)
    assert result.exit_code == 0
    assert "  Display Author Name" in result.output
