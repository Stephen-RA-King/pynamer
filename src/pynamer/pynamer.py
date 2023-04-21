#!/usr/bin/env python3
"""Example script to demonstrate layout and testing."""
# Core Library modules
import sys
from typing import Any

# Local modules
from . import logger


def handle_exception(exc_type, exc_value, exc_traceback):  # type: ignore
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def fizzbuzz(number_range: int) -> list:
    """Demonstrate one solution to the FizzBuzz problem.

    Return integers 1 to N, but print “Fizz” if an integer is divisible by 3,
    “Buzz” if an integer is divisible by 5, and “FizzBuzz” if an integer is
    divisible by both 3 and 5

    Parameters
    ----------
    number_range : int
        The maximum number that will be used

    Returns
    -------
    list
        The result will be returned as a list

    Examples
    --------
    >>> fizzbuzz(20)
    """
    result: list[Any] = []
    for num in range(1, number_range):
        if num % 15 == 0:
            result.append("FizzBuzz")
        elif num % 5 == 0:
            result.append("Buzz")
        elif num % 3 == 0:
            result.append("Fizz")
        else:
            result.append(num)
    logger.debug(f"fizzbuzz result: {result}")
    return result


def fibonacci(number_range: int) -> list:
    """series of numbers in which each number is the sum of the two that precede it.

    Parameters
    ----------
    number_range : int
        The maximum number that will be used

    Returns
    -------
    list
        The result will be returned as a list

    Examples
    --------
    >>> fibonacci(20)
    """

    result: list = []
    a, b = 1, 1
    while True:
        if a >= number_range:
            logger.debug(f"fibonacci result: {result}")
            return result
        result.append(a)
        a, b = b, (a + b)


def main():  # type: ignore
    print(fizzbuzz(20))
    print(fibonacci(20))


if __name__ == "__main__":
    raise SystemExit(main())
