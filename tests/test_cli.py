"""Тесты CLI через subprocess."""

import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Запустить CLI toolkit и вернуть результат."""
    command = [sys.executable, "-m", "toolkit", *args]
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check = False,
    )


def test_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "calc" in result.stdout
    assert "convert" in result.stdout


def test_calc_success():
    result = run_cli("calc", "3 * 13 + 77")
    assert result.returncode == 0
    assert result.stdout.strip() == "116"


def test_calc_error():
    result = run_cli("calc", "1019*/3")
    assert result.returncode == 2
    assert "Ошибка" in result.stderr


def test_convert_success():
    result = run_cli("convert", "1000", "--from", "mm", "--to", "m")
    assert result.returncode == 0
    assert result.stdout.strip() == "1"


def test_convert_error():
    result = run_cli("convert", "162", "--from", "kg", "--to", "m")
    assert result.returncode == 2
    assert "Ошибка" in result.stderr


def test_calc_division_error():
    result = run_cli("calc", "1 / 0")
    assert result.returncode == 2
    assert "Ошибка" in result.stderr







