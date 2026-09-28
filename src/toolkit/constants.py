OPERATOR_PRECEDENCE: dict[str, int] = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}

ALLOWED_OPERATOR_CHARS: str = "+-*/"

LENGTH_FACTORS: dict[str, float] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

MASS_FACTORS: dict[str, float] = {
    "g": 1.0,
    "kg": 1000.0,
}

TEMPERATURE_UNITS: set[str] = {"c", "f", "k"}

ABSOLUTE_ZERO_KELVIN: float = 0.0

UNIT_GROUPS: dict[str, set[str]] = {
    "length": {"mm", "cm", "m", "km"},
    "mass": {"g", "kg"},
    "temperature": {"c", "f", "k"},
}

EXIT_SUCCESS: int = 0

EXIT_ERROR: int = 2

PACKAGE_NAME: str = "toolkit"

PACKAGE_DESCRIPTION: str = "Консольный набор утилит: калькулятор и конвертер величин."
