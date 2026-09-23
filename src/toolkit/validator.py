"""Валидация арифметических выражений."""

from toolkit.errors import InvalidExpressionError


def validate(tokens: list) -> None:
    """Проверить последовательность токенов на корректность.

    Args:
        tokens: Список токенов вида (тип, значение), где тип —
            один из NUMBER, OPERATION, UNARY_OPERATION.

    Raises:
        InvalidExpressionError: Если выражение пустое, начинается
            с бинарного оператора, заканчивается оператором,
            содержит два бинарных оператора подряд, два числа
            подряд, или унарный оператор без числа после него.
    """
    if not tokens:
        raise InvalidExpressionError("Выражение пустое")
    elif tokens[0][0] == 'OPERATION':
        raise InvalidExpressionError(
            f"Символ {tokens[0][1]!r} недопустим вначале выражения"
        )
    elif (tokens[len(tokens) - 1][0] == 'OPERATION'
        or tokens[len(tokens) - 1][0] == 'UNARY_OPERATION'):
        raise InvalidExpressionError("Выражение заканчивается операцией")
    for i in range(len(tokens) - 1):
        if tokens[i][0] == 'OPERATION' and tokens[i + 1][0] == 'OPERATION':
            raise InvalidExpressionError("Две бинарные операции подряд")
        elif tokens[i][0] == 'NUMBER' and tokens[i + 1][0] == 'NUMBER':
            raise InvalidExpressionError("Два числа записаны подряд")
        elif ((tokens[i][0] == 'UNARY_OPERATION'
            and tokens[i + 1][0] == 'UNARY_OPERATION') or
            (tokens[i][0] == 'UNARY_OPERATION' and
            tokens[i + 1][0] == 'OPERATION')):
            raise InvalidExpressionError("Недопустимое сочетание операций")
