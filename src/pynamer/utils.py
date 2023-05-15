#!/usr/bin/env python3

# Core Library modules
import json
from pathlib import Path

# Third party modules
import requests
from packaging import version

# First party modules
import pynamer

# Local modules
from . import __version__, project_path
from .config import config


def _check_integrity():
    pass


def _reset():
    pass


def _check_version() -> tuple[version, str, bool]:
    """Utility function to compare package version against latest version on PyPI.

    Returns:
        current_version:    version of the installed package.
        str:                Message concerning the result of the comparison.
        bool:               True: if the installed package is up to date.
                            False: if there is a newer version on PyPI.
    """
    url_json = "".join([config.pypi_json_url, "pynamer", "/json"])
    current_version = version.parse(pynamer.__version__)
    try:
        project_json_raw = requests.get(url_json, timeout=10)
    except requests.RequestException as e:
        raise SystemExit("An error occurred with an HTTP request")
    if project_json_raw.status_code == 200:
        project_json = json.loads(project_json_raw.content)
        pypi_version = version.parse(project_json["info"]["version"])
        if pypi_version > current_version:
            return (
                current_version,
                f"(There is a newer version available: {pypi_version})",
                False,
            )
        elif pypi_version == current_version:
            return current_version, "(You have the most recent version)", True
