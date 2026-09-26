"""Конвертер единиц измерения."""
import json
from pathlib import Path
from toolkit.errors import (BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError)


def load_units() -> dict:
    """Загрузить таблицу конвертаций из файла units.json."""
    path = Path(__file__).parent.parent.parent / "units.json"
    with open(path) as file:
        return json.load(file)


units = load_units()


def convert(value: float | int, from_unit: str, to_unit: str) -> float | int:
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
    