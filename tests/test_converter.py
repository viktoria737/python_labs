import pytest

from toolkit.converter import convert
from toolkit.errors import ConverterError


class TestConverterPositive:

    def test_length_mm_to_cm(self) -> None:
        assert convert(10.0, "mm", "cm") == 1.0

    def test_length_km_to_m(self) -> None:
        assert convert(1.0, "km", "m") == 1000.0

    def test_mass_kg_to_g(self) -> None:
        assert convert(1.0, "kg", "g") == 1000.0

    def test_mass_g_to_kg(self) -> None:
        assert convert(500.0, "g", "kg") == 0.5

    def test_temperature_c_to_f(self) -> None:
        assert convert(0.0, "c", "f") == 32.0

    def test_temperature_f_to_c(self) -> None:
        assert convert(32.0, "f", "c") == pytest.approx(0.0)

    def test_temperature_c_to_k(self) -> None:
        assert convert(0.0, "c", "k") == pytest.approx(273.15)

    def test_temperature_k_to_c(self) -> None:
        assert convert(273.15, "k", "c") == pytest.approx(0.0)

    def test_case_insensitive(self) -> None:
        assert convert(1.0, "KM", "m") == 1000.0
        assert convert(100.0, "C", "F") == pytest.approx(212.0)


class TestConverterNegative:

    def test_unknown_unit(self) -> None:
        with pytest.raises(ConverterError, match="Неизвестная единица"):
            convert(1.0, "liters", "kg")

    def test_incompatible_units(self) -> None:
        with pytest.raises(ConverterError, match="Несовместимые единицы"):
            convert(1.0, "mm", "kg")

    def test_temperature_below_absolute_zero(self) -> None:
        with pytest.raises(ConverterError, match="абсолютного нуля"):
            convert(-300.0, "c", "k")

    def test_temperature_below_absolute_zero_fahrenheit(self) -> None:
        with pytest.raises(ConverterError, match="абсолютного нуля"):
            convert(-500.0, "f", "k")

    def test_unknown_target_unit(self) -> None:
        with pytest.raises(ConverterError, match="Неизвестная единица"):
            convert(1.0, "m", "parsecs")
