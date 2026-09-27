"""Точка входа CLI toolkit."""

import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def parse_number(text: str) -> int | float:
    """Преобразовать строку в int или float в зависимости от точки."""
    if '.' in text:
        return float(text)
    return int(text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="toolkit", 
        description="Калькулятор и конвертер.",
        epilog=(
            "Привет, дорогой друг, "
            "это инструкция по использованию "
            "калькулятора и конвертера"
            "\n"
            "Как пользоваться калькулятором: \n"
            "\n"
            "Тебе нужно написать данную команду в терминал "
            "python -m toolkit calc \"EXPRESSION\" \n"
            "\n"
            "На месте \"EXPRESSION\" ты должен писать своё "
            "арифметическое выражение в двойных кавычках \n"
            "\n"
            "Мой калькулятор умеет обрабатывать "
            "только данные команды: "
            "'*', '+', '-', '/' \n"
            "\n"
            "Примеры записи арифметического "
            "выражения: \"2 + 3 * 4\"; \n"
            "\"0012 + 023 * 23.5\"; \n"
            "\"2.0 * 225  /4 \". \n"
            "\n"
            "Как пользоваться конвертером: \n"
            "\n"
            "Тебе нужно написать данную команду в терминал "
            "python -m toolkit convert VALUE --from UNIT --to UNIT \n"
            "\n"
            "На месте VALUE ты должен писать своё "
            "значение, которое хочешь перевести \n"
            "\n"
            "На месте UNIT ты должен писать свою "
            "единицу измерения, из которой хочешь \n перевести"
            "введённое значение \n"
            "\n"
            "На месте UNIT, который идёт после "
            "обязательной команды --from "
            "ты должен писать свою единицу измерения, "
            "из которой хочешь \n"
            "перевести введённое значение \n"
            "\n"
            "На месте UNIT, который идёт после "
            "обязательной команды --to "
            "ты должен писать свою единицу измерения, "
            "в которую хочешь \n"
            "перевести введённое значение \n"
            "\n"
            "Мой конвертер умеет обрабатывать только данные "
            "единицы измерения: \n"
            "длина: `mm`, `cm`, `m`, `km`; \n"
            "масса: `g`, `kg`; \n"
            "температура: `c`, `f`, `k`. \n"
            "\n"
            "Примеры записи сообщения в "
            "конвертер: 1000 --from mm --to m; \n"
            "1.5 --from kg --to g; \n"
            "0 --from c --to f. \n"
        ), formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(
        dest="command", required=True)
    calc_parser = subparsers.add_parser(
        "calc", help="Вычислить арифметическое выражение.")
    calc_parser.add_argument(
        "expression", nargs = "?", default = "", help="Выражение")
    convert_parser = subparsers.add_parser(
        "convert", help="Сконвертировать значение между единицами.")
    convert_parser.add_argument(
        "value", type=parse_number, help="Числовое значение")
    convert_parser.add_argument(
        "--from", dest="from_unit", required=True, help="Откуда переводим")
    convert_parser.add_argument(
        "--to", dest="to_unit", required=True, help="Куда переводим")
    return parser


def run_calc(args: argparse.Namespace) -> int:
    """Выполнить команду calc и вернуть код выхода."""
    result = calculate(args.expression)
    print(result)
    return 0


def run_convert(args: argparse.Namespace) -> int:
    """Выполнить команду convert и вернуть код выхода."""
    result = convert(args.value, args.from_unit, args.to_unit)
    print(result)
    return 0


def main() -> int:
    """Точка входа: разобрать аргументы и выполнить команду."""
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "calc":
            return run_calc(args)
        if args.command == "convert":
            return run_convert(args)
    except ToolkitError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())