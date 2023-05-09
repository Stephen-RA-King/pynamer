#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_final_analysis_010(capsys):
    expected_output = (
        "┌─────────────────────────────────────────────────────────────────────────────┐\n"
        "│ FINAL "
        "ANALYSIS                                                              │\n"
        "├─────────────────────────────────────────────────────────────────────────────┤\n"
        "│ NOT "
        "AVAILABLE!                                                              │\n"
        "│                                                                             "
        "│\n"
        "│ A Gotcha!, whereby the package is not found even with PyPI's own "
        "search     │\n"
        "│ "
        "facility.                                                                   "
        "│\n"
        "│ It can only be found by searching the simple index which is not "
        "available   │\n"
        "│ through the "
        "interface                                                       │\n"
        "└─────────────────────────────────────────────────────────────────────────────┘"
    )

    pynamer._final_analysis([0, 1, 0])
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output.strip()


def test_final_analysis_110(capsys):
    expected_output = (
        "┌─────────────────────────────────────────────────────────────────────────────┐\n"
        "│ FINAL "
        "ANALYSIS                                                              │\n"
        "├─────────────────────────────────────────────────────────────────────────────┤\n"
        "│ NOT "
        "AVAILABLE!                                                              │\n"
        "│                                                                             "
        "│\n"
        "│ A Gotcha!, whereby the package is not found even with PyPI's own "
        "search     │\n"
        "│ "
        "facility.                                                                   "
        "│\n"
        "│ However if appears in the simple index and can be displayed by "
        "simply       │\n"
        "│ browsing to the projects "
        "URL                                                │\n"
        "└─────────────────────────────────────────────────────────────────────────────┘"
    )

    pynamer._final_analysis([1, 1, 0])
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output.strip()


def test_final_analysis_001(capsys):
    expected_output = (
        "┌──────────────────────────────────────────────────┐\n"
        "│ FINAL ANALYSIS                                   │\n"
        "├──────────────────────────────────────────────────┤\n"
        "│ NOT AVAILABLE!                                   │\n"
        "│                                                  │\n"
        "│ The package name was found in at least one place │\n"
        "└──────────────────────────────────────────────────┘"
    )

    pynamer._final_analysis([0, 0, 1])
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output.strip()


def test_final_analysis_000(capsys):
    expected_output = (
        "┌────────────────────────────────────────────────────┐\n"
        "│ FINAL ANALYSIS                                     │\n"
        "├────────────────────────────────────────────────────┤\n"
        "│ AVAILABLE!                                         │\n"
        "│                                                    │\n"
        "│ The package name was not found in any part of PyPI │\n"
        "└────────────────────────────────────────────────────┘"
    )

    pynamer._final_analysis([0, 0, 0])
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output.strip()
