"""Токенизация арифметических выражений."""

from toolkit.errors import InvalidExpressionError


def tokenize(expression: str) -> list:
    """Разбить арифметическое выражение на токены.

    Токены — кортежи (тип, значение). Типы: NUMBER, OPERATION,
    UNARY_OPERATION. Значение NUMBER — float, OPERATION — str,
    UNARY_OPERATION — str. Пробелы игнорируются.
    Точка допускается только внутри числа и должна 
    быть окружена цифрами.

    Args:
        expression: Строка с выражением, например "2 * 10 - 141.5".

    Returns:
        Список токенов в порядке появления в выражении.

    Raises:
        InvalidExpressionError: Если найден недопустимый символ
            или символ стоит в недопустимой позиции.
    """
    tokens = []
    state = 'START'
    current_token = ''
    for char in expression:
        # Начало нового токена
        if state == 'START':
            if char.isspace():
                continue
            elif char.isdigit():
                state = 'NUMBER'
                current_token = char
            elif char in '-+':
                state = 'UNARY_OPERATION'
                current_token = char
                tokens.append((state, current_token))
            elif char in '/*':
                state = 'OPERATION'
                current_token = char
                tokens.append((state, current_token))
            elif char == '.':
                raise InvalidExpressionError(
                    "Недопустимый символ для начала строки"
                )
            else:
                raise InvalidExpressionError(f"Недопустимый символ {char!r}")

        # Обрабатываем символ после цифры
        elif state == 'NUMBER':
            if char.isspace():
                tokens.append((state, float(current_token)))
                current_token = ''
                state = 'SPACE_AFTER_NUMBER'
            elif char == '.' and '.' not in current_token:
                state = 'DOT'
                current_token += char
            elif char == '.':
                raise InvalidExpressionError("В числе не может быть 2 точки")
            elif char.isdigit():
                state = 'NUMBER'
                current_token += char
            elif char in '-+/*':
                tokens.append((state, float(current_token)))
                state = 'OPERATION'
                current_token = char
                tokens.append((state, current_token))
            else:
                raise InvalidExpressionError(f"Недопустимый символ {char!r}")

        # Обрабатываем символ после пробела
        elif state in ('SPACE_AFTER_OPERATION', 'SPACE_AFTER_NUMBER'):
            if char.isspace():
                continue
            elif char in '-+' and state == 'SPACE_AFTER_OPERATION':
                state = 'UNARY_OPERATION'
                current_token = char
                tokens.append((state, current_token))
            elif char in '-+/*':
                state = 'OPERATION'
                current_token = char
                tokens.append((state, current_token))
            elif char.isdigit():
                state = 'NUMBER'
                current_token = char
            elif char == '.':
                raise InvalidExpressionError(
                    f"Символ {char!r} не может стоять после пробела"
                )
            else:
                raise InvalidExpressionError(f"Недопустимый символ {char!r}")

        # Обрабатываем символ после знака операции
        elif state in ('OPERATION', 'UNARY_OPERATION'):
            if char.isspace():
                current_token = ''
                state = 'SPACE_AFTER_OPERATION'
            elif char.isdigit():
                state = 'NUMBER'
                current_token = char
            elif char in '-+':
                state = 'UNARY_OPERATION'
                current_token = char
                tokens.append((state, current_token))
            elif char in '/*':
                state = 'OPERATION'
                current_token = char
                tokens.append((state, current_token))
            elif char == '.':
                raise InvalidExpressionError(
                    f"Символ {char!r} не допустим после знака операции"
                )
            else:
                raise InvalidExpressionError(f"Недопустимый символ {char!r}")

        # Ожидаем цифру после точки в числе
        elif state == 'DOT':
            if char.isdigit():
                state = 'NUMBER'
                current_token += char
            else:
                raise InvalidExpressionError(
                    f"Символ {char!r} недопустим после точки"
                )
    if state == 'NUMBER':
        tokens.append((state, float(current_token)))
    elif state == 'DOT':
        raise InvalidExpressionError("Число не может заканчиваться точкой")
    return tokens



