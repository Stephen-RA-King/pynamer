#!/usr/bin/env python3
# Core Library modules
import pickle
from pathlib import Path

# Third party modules
import pytest
import requests
from requests.exceptions import ConnectTimeout

# First party modules
from pynamer import pynamer, utils

BASE_DIR = Path(__file__).parents[0]


def my_custom_get(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "simple_index.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_generate_pypi_index(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get)
    monkeypatch.setattr(utils, "pypi_index_file_trv", BASE_DIR / "pypi_index")
    monkeypatch.setattr(
        utils, "project_count_file_trv", BASE_DIR / "project_count.pickle"
    )
    utils._generate_pypi_index()

    assert (BASE_DIR / "pypi_index").exists()
    assert (BASE_DIR / "project_count.pickle").exists()
    (BASE_DIR / "pypi_index").unlink()
    (BASE_DIR / "project_count.pickle").unlink()


def test_generate_pypi_index_error(monkeypatch, project_path_mock):
    def mock_requests_error(*args, **kwargs):
        raise ConnectTimeout("Connection timed out")

    monkeypatch.setattr(requests, "get", mock_requests_error)

    with pytest.raises(SystemExit) as excinfo:
        pynamer._generate_pypi_index()
    assert str(excinfo.value) == "An error occurred with an HTTP request"
