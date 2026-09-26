"""Ядро калькулятора: перевод в RPN и вычисление."""
from toolkit.errors import DivisionError, InvalidExpressionError
from toolkit.tokenizer import tokenize
from toolkit.validator import validate


def get_priority(token: tuple) -> int:
    """Вернуть приоритет оператора для shunting yard.

    Args:
        token: Токен вида (тип, символ).

    Returns:
        Приоритет: 3 для унарных операторов, 2 для умножения
        и деления, 1 для сложения и вычитания.

    Raises:
        InvalidExpressionError: Если токен не является оператором.
    """
    if token[0] == 'UNARY_OPERATION':
        return 3
    if token[0] == 'OPERATION' and token[1] in '*/':
        return 2
    if token[0] == 'OPERATION' and token[1] in '-+':
        return 1
    raise InvalidExpressionError(f"Нет приоритета для {token!r}")


def to_rpn(tokens: list) -> list:
    """Перевести токены в обратную польскую нотацию.

    Использует алгоритм shunting yard со стеком операторов.
    Числа сразу попадают в выходной список, операторы
    выталкиваются из стека по приоритету.

    Args:
        tokens: Список токенов из tokenizer.

    Returns:
        Список токенов в порядке обратной польской нотации.
    """
    rpn = []
    stack = []
    for token in tokens:
        if token[0] == 'NUMBER':
            rpn.append(token)
        else:
            while stack and get_priority(stack[-1]) >= get_priority(token):
                rpn.append(stack.pop())
            stack.append(token)
    while stack:
        rpn.append(stack.pop())
    return rpn


def operation(element: tuple, number1: float,
              number2: float | None) -> tuple:
    """Применить операцию к операндам.

    Для унарной операции используется только первый операнд,
    для бинарной — оба. Порядок операндов: number1 — правый
    (первый из стека), number2 — левый (второй из стека).

    Args:
        element: Токен операции вида (тип, символ).
        number1: Правый операнд.
        number2: Левый операнд или None для унарной операции.

    Returns:
        Токен ('NUMBER', результат) с результатом операции.

    Raises:
        DivisionError: Если правый операнд равен нулю.
        InvalidExpressionError: Если операция неизвестна.
    """
    if element[0] == 'UNARY_OPERATION':
        if element[1] == '+':
            return ('NUMBER', number1)
        if element[1] == '-':
            return ('NUMBER', -number1)
    else:
        if element[1] == '+':
            return ('NUMBER', number2 + number1)
        if element[1] == '-':
            return ('NUMBER', number2 - number1)
        if element[1] == '*':
            return ('NUMBER', number2 * number1)
        if element[1] == '/':
            if number1 == 0:
                raise DivisionError("Деление на ноль")
            return ('NUMBER', number2 / number1)
    raise InvalidExpressionError(f"Неизвестная операция: {element[1]!r}")


def evaluate(rpn: list) -> float:
    """Вычислить выражение в обратной польской нотации.

    Использует стек значений: числа кладутся в стек, операторы
    достают нужное количество операндов и кладут результат.

    Args:
        rpn: Список токенов в RPN из to_rpn.

    Returns:
        Результат вычисления в виде float.
    """
    stack = []
    for element in rpn:
        if element[0] == 'NUMBER':
            stack.append(element)
        elif element[0] == 'UNARY_OPERATION':
            stack.append(operation(element, stack.pop()[1], None))
        elif element[0] == 'OPERATION':
            stack.append(operation(element, stack.pop()[1], stack.pop()[1]))
    return stack[-1][1]


def calculate(expression: str) -> float:
    """Вычислить значение арифметического выражения.

    Связывает все этапы: токенизация, валидация, перевод
    в RPN, вычисление.

    Args:
        expression: Строка с выражением, например "2 + 3 * 4".

    Returns:
        Результат вычисления в виде float.

    Raises:
        InvalidExpressionError: Если выражение некорректно.
        DivisionError: Если в выражении есть деление на ноль.
    """
    tokens = tokenize(expression)
    validate(tokens)
    rpn = to_rpn(tokens)
    return evaluate(rpn)
