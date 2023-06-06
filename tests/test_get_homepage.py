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


data1 = {"info": {"home_page": "https://github.com/stephen-ra-king/pynball"}}

data2 = {"info": {"home_page": "https://pycqa.github.io/isort/"}}

data3 = {
    "info": {
        "home_page": "https://requests.readthedocs.io/",
        "source": "https://github.com/psf/requests",
    }
}

data4 = {"info": {"home_page": "https://requests.readthedocs.io/"}}

data5 = {"info": {"home_page": ""}}


def test_homepage_test1():
    result = pynamer.validators._get_homepage(data1, "pynball")
    assert result == (
        "Homepage: https://github.com/stephen-ra-king/pynball",
        "https://github.com/stephen-ra-king/pynball",
    )


def test_homepage_test2():
    result = pynamer.validators._get_homepage(data2, "isort")
    assert result == (
        "Homepage: https://github.com/pycqa/isort",
        "https://github.com/pycqa/isort",
    )


def test_homepage_test3():
    result = pynamer.validators._get_homepage(data3, "requests")
    assert result == (
        "Homepage: https://github.com/psf/requests",
        "https://github.com/psf/requests",
    )


def test_homepage_test4():
    result = pynamer.validators._get_homepage(data4, "requests")
    assert result == (
        "Homepage: https://requests.readthedocs.io/",
        "https://requests.readthedocs.io/",
    )


def test_homepage_test5():
    result = pynamer.validators._get_homepage(data5, "requests")
    assert result == (
        "Homepage: None",
        "",
    )
