#!/usr/bin/env python3
# Core Library modules
import pickle
import shutil
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_pypi_search_index(monkeypatch):
    monkeypatch.setattr(pynamer, "project_path", BASE_DIR / "resources")
    assert pynamer._pypi_search_index("pynball") is True
    assert pynamer._pypi_search_index("zeedonk") is False
