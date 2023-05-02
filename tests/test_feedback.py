#!/usr/bin/env python3
# Core Library modules

# Third party modules
import pytest

# First party modules
from pynamer import pynamer


@pytest.mark.parametrize(
    "message, message_type, result",
    [
        ("this is a null message", "null", "None"),
        ("this is a nominal message", "nominal", "None"),
        ("this is a warning message", "warning", "None"),
        ("this is an error message", "error", "None"),
        ("this is an error message", "wrong", "None"),
    ],
)
def test_feedback(message, message_type, result):
    """Pytest test to assert mark parametrize pytest feature."""
    assert result == str(pynamer._feedback(message, message_type))
