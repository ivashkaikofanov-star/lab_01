"""Обработка ошибок с помощью классов."""

class ToolkitError(Exception):
    """Главная ветка всех ошибок."""


class DivisionError(ToolkitError):
    """Деление на ноль."""


class InvalidExpressionError(ToolkitError):
    """Найден недопустимый символ в арифметическом
    выражении или символ стоит в неправильной позиции.
    """


class UnknownUnitError(ToolkitError):
    """Неизвестная единица измерения."""


class BelowAbsoluteZeroError(ToolkitError):
    """Температура ниже абсолютного нуля."""


class IncompatibleUnitsError(ToolkitError):
    """Несовместимые единицы измерения."""


