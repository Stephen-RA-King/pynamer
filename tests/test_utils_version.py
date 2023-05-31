#!/usr/bin/env python3
# Core Library modules
import pickle
from pathlib import Path

# Third party modules
import pytest
import requests
from colorama import Back, Fore, Style
from requests.exceptions import ConnectTimeout

# First party modules
import pynamer

BASE_DIR = Path(__file__).parents[0]


def my_custom_get_found(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "requests_get_json_pynamer.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_utils_version_old(monkeypatch, capfd):
    monkeypatch.setattr(requests, "get", my_custom_get_found)
    monkeypatch.setattr(pynamer, "__version__", "1.0.0")
    result = f"{Fore.YELLOW}{Back.BLACK}{Style.BRIGHT}1.0.0 : (There is a newer version available: 1.1.0){Style.RESET_ALL}\n"
    pynamer.utils._check_version()
    captured = capfd.readouterr()
    assert captured.out == result


def test_utils_version(monkeypatch, capfd):
    monkeypatch.setattr(requests, "get", my_custom_get_found)
    monkeypatch.setattr(pynamer, "__version__", "1.1.0")
    result = f"{Fore.GREEN}{Style.BRIGHT}1.1.0 : (You have the most recent version){Style.RESET_ALL}\n"
    pynamer.utils._check_version()
    captured = capfd.readouterr()
    assert captured.out == result


def test_ping_json_error(monkeypatch):
    def mock_requests_error(*args, **kwargs):
        raise ConnectTimeout("Connection timed out")

    monkeypatch.setattr(requests, "get", mock_requests_error)
    with pytest.raises(SystemExit) as excinfo:
        pypi_version, message, result = pynamer.utils._check_version()
    assert str(excinfo.value) == "An error occurred with an HTTP request"
