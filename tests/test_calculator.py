import pytest

from toolkit.calculator import calculate
from toolkit.errors import CalculatorError


class TestCalculatorPositive:

    def test_simple_addition(self) -> None:
        assert calculate("2 + 3") == 5.0

    def test_simple_subtraction(self) -> None:
        assert calculate("10 - 4") == 6.0

    def test_multiplication(self) -> None:
        assert calculate("3 * 4") == 12.0

    def test_division(self) -> None:
        assert calculate("10 / 4") == 2.5

    def test_operator_precedence(self) -> None:
        assert calculate("2 + 3 * 4") == 14.0
        assert calculate("2 * 3 + 4") == 10.0
        assert calculate("10 - 6 / 2") == 7.0

    def test_float_numbers(self) -> None:
        assert calculate("1.5 + 2.5") == 4.0
        assert calculate("0.1 * 0.1") == pytest.approx(0.01)

    def test_unary_minus(self) -> None:
        assert calculate("-5") == -5.0
        assert calculate("-5 + 3") == -2.0

    def test_unary_plus(self) -> None:
        assert calculate("+5") == 5.0
        assert calculate("+5 + 3") == 8.0

    def test_spaces_ignored(self) -> None:
        assert calculate("2+3") == 5.0
        assert calculate("  2   +     3  ") == 5.0

    def test_complex_expression(self) -> None:
        assert calculate("2 + 3 * 4 - 6 / 2") == 11.0

    def test_unary_minus_after_operator(self) -> None:
        assert calculate("5 + -3") == 2.0
        assert calculate("5 * -2") == -10.0


class TestCalculatorNegative:

    def test_empty_expression(self) -> None:
        with pytest.raises(CalculatorError, match="Пустое выражение"):
            calculate("")

    def test_empty_spaces_only(self) -> None:
        with pytest.raises(CalculatorError, match="Пустое выражение"):
            calculate("   ")

    def test_invalid_character(self) -> None:
        with pytest.raises(CalculatorError, match="Недопустимый символ"):
            calculate("2 + a")

    def test_division_by_zero(self) -> None:
        with pytest.raises(CalculatorError, match="Деление на ноль"):
            calculate("5 / 0")

    def test_two_operators_in_row(self) -> None:
        with pytest.raises(CalculatorError, match="Два бинарных оператора"):
            calculate("5 + * 3")

    def test_missing_operand_end(self) -> None:
        with pytest.raises(CalculatorError, match="Пропущенный операнд"):
            calculate("5 +")

    def test_missing_operand_beginning(self) -> None:
        with pytest.raises(CalculatorError, match="Пропущенный операнд"):
            calculate("* 5")

    def test_double_dot_in_number(self) -> None:
        with pytest.raises(CalculatorError, match="Некорректное число"):
            calculate("1.2.3 + 5")
