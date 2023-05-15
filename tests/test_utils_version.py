#!/usr/bin/env python3
# Core Library modules
import pickle
from pathlib import Path

# Third party modules
import pytest
import requests
from requests.exceptions import ConnectTimeout

# First party modules
import pynamer

BASE_DIR = Path(__file__).parents[0]


def my_custom_get_found(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "requests_get_json_pynamer.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_utils_version_old(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get_found)
    monkeypatch.setattr(pynamer, "__version__", "1.0.0")

    pypi_version, message, result = pynamer.utils._check_version()

    assert str(pypi_version) == "1.0.0"
    assert message == "(There is a newer version available: 1.1.0)"
    assert result is False


def test_utils_version(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get_found)
    monkeypatch.setattr(pynamer, "__version__", "1.1.0")

    pypi_version, message, result = pynamer.utils._check_version()

    assert str(pypi_version) == "1.1.0"
    assert message == "(You have the most recent version)"
    assert result is True


def test_ping_json_error(monkeypatch):
    def mock_requests_error(*args, **kwargs):
        raise ConnectTimeout("Connection timed out")

    monkeypatch.setattr(requests, "get", mock_requests_error)

    with pytest.raises(SystemExit) as excinfo:
        pypi_version, message, result = pynamer.utils._check_version()
    assert str(excinfo.value) == "An error occurred with an HTTP request"
