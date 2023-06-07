#!/usr/bin/env python3
# Core Library modules

# Core Library modules


# First party modules
from pynamer import pynamer


def test_is_valid_package_name_true():
    assert pynamer._is_valid_package_name("pynball") is True


def test_is_valid_package_name_false():
    assert pynamer._is_valid_package_name("pynball!") is False
