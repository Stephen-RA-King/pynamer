#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# First party modules
from pynamer import pynamer, validators

BASE_DIR = Path(__file__).parents[0]


def test_pypi_search_index(monkeypatch):
    monkeypatch.setattr(pynamer, "project_path", BASE_DIR / "resources")
    monkeypatch.setattr(
        validators, "pypi_index_file_trv", BASE_DIR / "resources" / "pypi_index"
    )
    assert pynamer._pypi_search_index("pynball") is True
    assert pynamer._pypi_search_index("zeedonk") is False
