from toolkit.errors import DivisionError, InvalidExpressionError
from toolkit.tokenizer import tokenize
from toolkit.validator import validate


def get_priority(token: tuple) -> int:
    if token[0] == 'UNARY_OPERATION':
        return 3
    if token[0] == 'OPERATION' and token[1] in '*/':
        return 2
    if token[0] == 'OPERATION' and token[1] in '-+':
        return 1
    raise InvalidExpressionError(f"Нет приоритета для {token!r}")


def to_rpn(tokens: list) -> list:
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


def evalute(rpn: list) -> float:
    stack = []
    for element in rpn:
        if element[0] == 'NUMBER':
            stack.append(element)
        else:
            stack.pop()