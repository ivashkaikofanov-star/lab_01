"""Конвертер единиц измерения."""

import json
from pathlib import Path

from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)


def load_units() -> dict:
    """Загрузить таблицу конвертаций из файла units.json."""
    path = Path(__file__).parent.parent.parent / "units.json"
    with open(path) as file:
        return json.load(file)


units = load_units()


def convert(value: float | int, from_unit: str, to_unit: str) -> float | int:
    """Перевести значение из одной единицы измерения в другую.

    Поддерживает длину (mm, cm, m, km), массу (g, kg) и температуру
    (c, f, k). Регистр единиц не учитывается. Конвертация между
    разными группами запрещена. Для температуры значение не может
    быть ниже абсолютного нуля.

    Args:
        value: Значение.
        from_unit: Из какой единицы ищмерения переводим.
        to_unit: В какую единицу измерения переводим .

    Returns:
        Сконвертированное значение. Если value — int и результат
        целый, возвращается int, иначе — float.

    Raises:
        UnknownUnitError: Если ввели неизвестную единицу измерения.
        IncompatibleUnitsError: Если единицы измерения из разных групп.
        BelowAbsoluteZeroError: Если температура ниже абсолютного нуля.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    if from_unit not in units:
        raise UnknownUnitError(f"Единица измерения {from_unit!r} не найдена")
    if to_unit not in units:
        raise UnknownUnitError(f"Единица измерения {to_unit!r} не найдена")
    if units[from_unit]["group"] != units[to_unit]["group"]:
        raise IncompatibleUnitsError(
            f"Единицы измерения {to_unit!r} и {from_unit!r} несовместимы"
        )
    base = (units[from_unit]["coefficient"] * value +
            units[from_unit]["shift"])
    if units[from_unit]["group"] == "temperature" and base < -273.15:
        raise BelowAbsoluteZeroError("Температура ниже абсолютного нуля")
    result = (base - units[to_unit]["shift"]) / units[to_unit]["coefficient"]
    if isinstance(value, int) and result.is_integer():
        return int(result)
    return float(result)
