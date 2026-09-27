"""Негативные тесты калькулятора."""

import pytest

from toolkit.calculator import calculate
from toolkit.errors import DivisionError, InvalidExpressionError


def test_division_zero():
    with pytest.raises(DivisionError):
        calculate("224 / 0")


def test_empty_expression():
    with pytest.raises(InvalidExpressionError):
        calculate("")


def test_two_operators():
    with pytest.raises(InvalidExpressionError):
        calculate("67 */ 321")


def test_invalid_symbol():
    with pytest.raises(InvalidExpressionError):
        calculate("7 + s")


def test_two_numbers():
    with pytest.raises(InvalidExpressionError):
        calculate("114 344")


def test_ends_operator():
    with pytest.raises(InvalidExpressionError):
        calculate("23 +")


def test_starts_binary_operator():
    with pytest.raises(InvalidExpressionError):
        calculate("* 2")


def test_ends_dot():
    with pytest.raises(InvalidExpressionError):
        calculate("6.")


def test_two_dots():
    with pytest.raises(InvalidExpressionError):
        calculate("2.5.67")
