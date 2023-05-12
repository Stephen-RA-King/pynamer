#!/usr/bin/env python3
# Core Library modules

# Core Library modules


# First party modules
from pynamer import pynamer


def test_is_valid_package_name():
    assert pynamer._is_valid_package_name("pynball") is True
    assert pynamer._is_valid_package_name("1pynball") is False
