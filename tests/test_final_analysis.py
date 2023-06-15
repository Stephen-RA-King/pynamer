#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# Third party modules
from rich.console import Console
from rich.table import Table

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_final_analysis_010(capsys):
    table = Table(show_header=True)
    table.add_column("FINAL ANALYSIS", style="bold cyan")
    table.add_row("[red]NOT AVAILABLE![/red]\n")
    table.add_row(
        "A Gotcha!, whereby the package is not found even with PyPI's own search"
        " facility.\n"
        "It can only be found by searching the simple index which is not available "
        "through the web interface.\n\n"
        "The most likely cause is an abandoned or deleted project by the owner.\n\n"
        "Refer to PEP 541 – 'Package Index Name Retention' for details pertaining "
        "to name transfer.\n"
        "https://peps.python.org/pep-0541/#how-to-request-a-name-transfer"
    )
    console = Console()
    console.print(table)
    captured_expected = capsys.readouterr()

    pynamer._final_analysis([0, 1, 0])
    captured_actual = capsys.readouterr()

    assert captured_actual.out.strip() == captured_expected.out.strip()


def test_final_analysis_110(capsys):
    table = Table(show_header=True)
    table.add_column("FINAL ANALYSIS", style="bold cyan")
    table.add_row("[red]NOT AVAILABLE![/red]\n")
    table.add_row(
        "A Gotcha!, whereby the package is not found even with PyPI's own search"
        " facility.\n"
        "However if appears in the simple index and can be displayed by simply"
        " browsing "
        "to the projects URL"
    )
    console = Console()
    console.print(table)
    captured_expected = capsys.readouterr()

    pynamer._final_analysis([1, 1, 0])
    captured_actual = capsys.readouterr()

    assert captured_actual.out.strip() == captured_expected.out.strip()


def test_final_analysis_001(capsys):
    table = Table(show_header=True)
    table.add_column("FINAL ANALYSIS", style="bold cyan")
    table.add_row("[red]NOT AVAILABLE![/red]\n")
    table.add_row("The package name was found in at least one place")
    console = Console()
    console.print(table)
    captured_expected = capsys.readouterr()

    pynamer._final_analysis([0, 0, 1])
    captured_actual = capsys.readouterr()

    assert captured_actual.out.strip() == captured_expected.out.strip()


def test_final_analysis_000(capsys):
    table = Table(show_header=True)
    table.add_column("FINAL ANALYSIS", style="bold cyan")
    table.add_row("[green]AVAILABLE![/green]\n")
    table.add_row("The package name was not found in any part of PyPI")
    console = Console()
    console.print(table)
    captured_expected = capsys.readouterr()

    pynamer._final_analysis([0, 0, 0])
    captured_actual = capsys.readouterr()

    assert captured_actual.out.strip() == captured_expected.out.strip()
