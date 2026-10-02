from toolkit.constants import ALLOWED_OPERATOR_CHARS, OPERATOR_PRECEDENCE
from toolkit.errors import CalculatorError

NUMBER_TOKEN = "NUMBER"
OPERATOR_TOKEN = "OPERATOR"
UNARY_OPERATOR_TOKEN = "UNARY_OPERATOR"


class Token:
    """Представление одного токена в выражении."""
    def __init__(self, token_type: str, value: str, position: int) -> None:
        """Инициализирование токена."""
        self.type = token_type
        self.value = value
        self.position = position

    def __repr__(self) -> str:
        """Строковое представление для отладки."""
        return f"Token({self.type!r}, {self.value!r}, pos={self.position})"

    def __eq__(self, other: object) -> bool:
        """Сравнение токенов по всем параметрам."""
        if not isinstance(other, Token):
            return NotImplemented
        return (
            self.type == other.type
            and self.value == other.value
            and self.position == other.position
        )


def tokenize(expression: str) -> list[Token]:
    """Разбивание строки выражения на список токенов."""
    if not expression or expression.strip() == "":
        raise CalculatorError("Пустое выражение")

    tokens: list[Token] = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit() or char == ".":
            start = i
            has_dot = False
            while i < n and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    if has_dot:
                        raise CalculatorError(
                            f"Некорректное число: две точки в позиции {i}"
                        )
                    has_dot = True
                i += 1
            num_str = expression[start:i]
            if num_str == ".":
                raise CalculatorError("Некорректное число")
            tokens.append(Token(NUMBER_TOKEN, num_str, start))
            continue
        if char in ALLOWED_OPERATOR_CHARS:
            if char in "+-" and (
                len(tokens) == 0
                or tokens[-1].type in (OPERATOR_TOKEN, UNARY_OPERATOR_TOKEN)
            ):
                tokens.append(Token(UNARY_OPERATOR_TOKEN, char, i))
            else:
                tokens.append(Token(OPERATOR_TOKEN, char, i))
            i += 1
            continue
        raise CalculatorError(f"Недопустимый символ {char!r}")

    return tokens


def validate_tokens(tokens: list[Token]) -> None:
    """Проверка на корректность последовательности токенов."""
    if len(tokens) == 0:
        raise CalculatorError("Пустое выражение")
    for idx, token in enumerate(tokens):
        if (
            token.type == OPERATOR_TOKEN
            and idx > 0
            and tokens[idx - 1].type == OPERATOR_TOKEN
        ):
            raise CalculatorError(
                f"Два бинарных оператора подряд в позиции {token.position}"
            )
        if token.type == OPERATOR_TOKEN and idx == 0:
            raise CalculatorError(
                f"Пропущенный операнд перед оператором в позиции {token.position}"
            )
        if (
            token.type == OPERATOR_TOKEN
            and idx > 0
            and tokens[idx - 1].type == UNARY_OPERATOR_TOKEN
            and token.value not in ("+", "-")
        ):
            raise CalculatorError(f"Пропущенный операнд в позиции {token.position}")
    if tokens[-1].type in (OPERATOR_TOKEN, UNARY_OPERATOR_TOKEN):
        raise CalculatorError("Пропущенный операнд в конце выражения")


def to_rpn(tokens: list[Token]) -> list[Token]:
    """Преобразование токенов в обратную польскую запись (RPN)."""
    output: list[Token] = []
    operator_stack: list[Token] = []
    for token in tokens:
        if token.type == NUMBER_TOKEN:
            output.append(token)
        elif token.type == UNARY_OPERATOR_TOKEN:
            if token.value == "-":
                operator_stack.append(Token(UNARY_OPERATOR_TOKEN, "u-", token.position))
        elif token.type == OPERATOR_TOKEN:
            while (
                operator_stack
                and operator_stack[-1].type
                in (OPERATOR_TOKEN, UNARY_OPERATOR_TOKEN)
            ):
                top = operator_stack[-1]
                if top.type == UNARY_OPERATOR_TOKEN or (
                    OPERATOR_PRECEDENCE[top.value]
                    >= OPERATOR_PRECEDENCE[token.value]
                ):
                    output.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(token)
    while operator_stack:
        output.append(operator_stack.pop())

    return output


def evaluate_rpn(rpn: list[Token]) -> float:
    """Вычисление значения выражения, заданного в RPN."""
    stack: list[float] = []
    for token in rpn:
        if token.type == NUMBER_TOKEN:
            try:
                stack.append(float(token.value))
            except ValueError:
                raise CalculatorError(f"Неверное числовое значение: {token.value}")
        elif token.type == OPERATOR_TOKEN:
            if len(stack) < 2:
                raise CalculatorError("Пропущенный операнд")
            b = stack.pop()
            a = stack.pop()
            if token.value == "+":
                stack.append(a + b)
            elif token.value == "-":
                stack.append(a - b)
            elif token.value == "*":
                stack.append(a * b)
            elif token.value == "/":
                if b == 0:
                    raise CalculatorError("Деление на ноль")
                stack.append(a / b)
        elif token.type == UNARY_OPERATOR_TOKEN and token.value == "u-":
            if len(stack) < 1:
                raise CalculatorError("Пропущенный операнд для унарного минуса")
            a = stack.pop()
            stack.append(-a)
    if len(stack) != 1:
        raise CalculatorError("Некорректное выражение")

    return stack[0]


def calculate(expression: str) -> float:
    """Вычисление арифметического выражения."""
    tokens = tokenize(expression)
    validate_tokens(tokens)
    rpn = to_rpn(tokens)
    return evaluate_rpn(rpn)
