class ToolkitError(Exception):
    """Базовое исключение для всех ошибок пакета toolkit."""

class CalculatorError(ToolkitError):
    """Ошибка, возникшая при вычислении выражения калькулятором."""

class ConverterError(ToolkitError):
    """Ошибка, возникшая при конвертации величин."""
