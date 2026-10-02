from toolkit.constants import (
    ABSOLUTE_ZERO_KELVIN,
    LENGTH_FACTORS,
    MASS_FACTORS,
    UNIT_GROUPS,
)
from toolkit.errors import ConverterError


def find_unit_group(unit: str) -> str:
    """Определение группы, к которой принадлежит единица."""
    for group_name, units in UNIT_GROUPS.items():
        if unit in units:
            return group_name
    raise ConverterError(f"Неизвестная единица: {unit}")


def convert_linear(
        value: float, from_unit: str, to_unit: str, factors: dict[str, float]
) -> float:
    """Конвертирование линейной величины (длина или масса).
    Приводит значение к базовой единице, затем из базовой в целевую."""
    base_value = value * factors[from_unit]
    return base_value / factors[to_unit]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Конвертирование температуры между шкалами Цельсия, Фаренгейта и Кельвина."""
    if from_unit == "k":
        kelvin = value
    elif from_unit == "c":
        kelvin = value + 273.15
    elif from_unit == "f":
        kelvin = (value - 32.0) * 5.0 / 9.0 + 273.15
    else:
        raise ConverterError(f"Неизвестная единица температуры: {from_unit}")
    if kelvin < ABSOLUTE_ZERO_KELVIN:
        raise ConverterError("Температура ниже абсолютного нуля")
    if to_unit == "k":
        return kelvin
    elif to_unit == "c":
        return kelvin - 273.15
    elif to_unit == "f":
        return (kelvin - 273.15) * 9.0 / 5.0 + 32.0
    else:
        raise ConverterError(f"Неизвестная единица температуры: {to_unit}")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Конвертирование величины из одной единицы в другую."""
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    from_group = find_unit_group(from_unit_lower)
    to_group = find_unit_group(to_unit_lower)
    if from_group != to_group:
        raise ConverterError(f"Несовместимые единицы: {from_unit} и {to_unit}")
    if from_group == "temperature":
        return convert_temperature(value, from_unit_lower, to_unit_lower)
    elif from_group == "length":
        return convert_linear(value, from_unit_lower, to_unit_lower, LENGTH_FACTORS)
    elif from_group == "mass":
        return convert_linear(value, from_unit_lower, to_unit_lower, MASS_FACTORS)
    else:
        raise ConverterError(f"Неизвестная единица: {from_group}")
