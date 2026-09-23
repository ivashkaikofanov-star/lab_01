"""Обработка ошибок с помощью классов."""

class ToolkitError(Exception):
    """Главная ветка всех ошибок."""


class DivisionByZeroError(ToolkitError):
    """Деление на ноль."""


class InvalidExpressionError(ToolkitError):
    """Найден недопустимый символ в арифметическом
    выражении или символ стоит в неправильной позиции.
    """


class IncorrectUnitError(ToolkitError):
    """Неизвестная единица измерения."""


class BellowZeroError(ToolkitError):
    """Температура ниже абсолютного нуля."""


class IncompatibleUnitsError(ToolkitError):
    """Несовместимые единицы измерения."""


