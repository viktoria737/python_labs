import subprocess
import sys


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Запустить CLI toolkit с заданными аргументами."""
    return subprocess.run(
        [sys.executable, "-m", "toolkit"] + args,
        capture_output=True,
        text=True,
        check=False
    )


class TestCli:

    def test_help_exits_zero(self) -> None:
        """Команда --help завершается с кодом 0."""
        result = run_cli(["--help"])
        assert result.returncode == 0
        assert "toolkit" in result.stdout

    def test_calc_success(self) -> None:
        """Успешное вычисление возвращает код 0 и результат."""
        result = run_cli(["calc", "2 + 3"])
        assert result.returncode == 0
        assert "5" in result.stdout

    def test_calc_error_exit_code(self) -> None:
        """Ошибка калькулятора возвращает код 2 и пишет в stderr."""
        result = run_cli(["calc", "5 / 0"])
        assert result.returncode == 2
        assert "Деление на ноль" in result.stderr

    def test_convert_success(self) -> None:
        """Успешная конвертация возвращает код 0."""
        result = run_cli(["convert", "1", "--from", "km", "--to", "m"])
        assert result.returncode == 0
        assert "1000.0" in result.stdout

    def test_convert_error_exit_code(self) -> None:
        """Ошибка конвертации возвращает код 2 и пишет в stderr."""
        result = run_cli(["convert", "1", "--from", "mm", "--to", "kg"])
        assert result.returncode == 2
        assert "Несовместимые" in result.stderr
