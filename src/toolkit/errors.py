class ToolkitError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class CalculatorError(ToolkitError):
    pass


class ConverterError(ToolkitError):
    pass
