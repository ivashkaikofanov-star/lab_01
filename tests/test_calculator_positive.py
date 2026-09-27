"""Позитивные тесты калькулятора."""

from pytest import approx

from toolkit.calculator import calculate


def test_priority():
    assert calculate("67 + 39 * 4") == 223


def test_division_float():
    assert calculate("10 / 4") == approx(2.5)


def test_unary_operation():
    assert calculate("-26 * -3") == 78


def test_binary_plus_unary():
    assert calculate("1 + -1012") == -1011


def test_spaces_ignored():
    assert calculate(" 2 +    67+    3 ") == 72


def test_floats():
    assert calculate("2.51 + 3.47 + 67") == approx(72.98)


def test_extra_zeros():
    assert calculate("00024 + 23.00 * 6.70000") == approx(178.1)


def test_big_expression():
    assert calculate("-23 * 001.0 / 23 *- 245.214 ++ 67") == approx(312.214)