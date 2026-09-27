"""Позитивные и негативные тесты конвертера."""

import pytest

from toolkit.converter import convert
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)


def test_mm_to_m():
    assert convert(2500, "mm", "m") == pytest.approx(2.5)


def test_kg_to_g():
    assert convert(1.5, "kg", "g") == 1500.0


def test_c_to_f():
    assert convert(2.5, "c", "f") == pytest.approx(36.5)


def test_absolute_zero():
    assert convert(-273.15, "c", "k") == pytest.approx(0.0)


def test_uppercase_units():
    assert convert(12, "M", "CM") == 1200


def test_m_to_cm():
    assert convert(2, "m", "cm") == 200


def test_same_unit():
    assert convert(67, "m", "m") == 67


def test_incompatible_units():
    with pytest.raises(IncompatibleUnitsError):
        convert(26, "kg", "m")


def test_below_absolute_zero():
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-348, "c", "k")


def test_unknown_unit():
    with pytest.raises(UnknownUnitError):
        convert(1000, "s", "m")




