#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_pypi_search_index(monkeypatch):
    expected_results_file = BASE_DIR / "resources" / "output_file"
    output_file = BASE_DIR / "output_file"
    result_dict = {"pyball": [1, 1, 1]}
    pynamer._write_output_file(str(output_file), result_dict)

    with open(expected_results_file) as f:
        expected_text = f.read()
    with open(output_file) as f:
        result_text = f.read()

    assert result_text == expected_text

    output_file.unlink()
