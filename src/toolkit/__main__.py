import argparse
import sys

from toolkit.constants import (
    EXIT_ERROR,
    EXIT_SUCCESS,
    PACKAGE_DESCRIPTION,
    PACKAGE_NAME,
)
from toolkit.errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    """Создание парсера аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog=PACKAGE_NAME,
        description=PACKAGE_DESCRIPTION,
    )
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")
    calc_parser = subparsers.add_parser(
        "calc", help="Вычислить арифметическое выражение"
    )
    calc_parser.add_argument(
        "expression", type=str, help="Арифметическое выражение в кавычках"
    )
    convert_parser = subparsers.add_parser(
        "convert", help="Конвертировать величину"
    )
    convert_parser.add_argument(
        "value", type=str, help="Численное значение для конвертации"
    )
    convert_parser.add_argument(
        "--from", dest="from_unit", required=True, type=str, help="Исходная единица"
    )
    convert_parser.add_argument(
        "--to", dest="to_unit", required=True, type=str, help="Целевая единица"
    )
    return parser


def handle_calc(expression: str) -> int:
    """Обработка команды calc."""
    from toolkit.calculator import calculate

    try:
        result = calculate(expression)
        if result == int(result):
            print(int(result))
        else:
            print(result)
        return EXIT_SUCCESS
    except ToolkitError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return EXIT_ERROR


def handle_convert(value_str: str, from_unit: str, to_unit: str) -> int:
    """Обработка команды convert."""
    from toolkit.converter import convert

    try:
        value = float(value_str)
        result = convert(value, from_unit, to_unit)
        print(result)
        return EXIT_SUCCESS
    except ToolkitError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return EXIT_ERROR
    except ValueError:
        print(f"Ошибка: неверное числовое значение: {value_str}", file=sys.stderr)
        return EXIT_ERROR


def main() -> int:
    """Главная точка входа CLI.
    Разбирает аргументы, вызывает нужную подкоманду и возвращает код возврата."""
    parser = build_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return EXIT_SUCCESS
    if args.command == "calc":
        return handle_calc(args.expression)
    if args.command == "convert":
        return handle_convert(args.value, args.from_unit, args.to_unit)
    parser.print_help()
    return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
