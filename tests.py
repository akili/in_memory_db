import io
import sys

import pytest
from _pytest.capture import CaptureFixture

from exceptions import UserInputError
from main import TinyDBCli


def run_multiple_commands(commands: str) -> None:
    """Передаем пачку комманд в приложение."""
    app = TinyDBCli()
    stdin_backup = sys.stdin
    sys.stdin = io.StringIO(commands)
    app.cmdloop()
    sys.stdin = stdin_backup


def test_eof_exit(capsys: CaptureFixture) -> None:
    """Проверка работы ctrl+d."""
    app = TinyDBCli()

    app.do_EXIT()

    captured = capsys.readouterr()
    assert "Пока!" in captured.out


def test_set(capsys: CaptureFixture) -> None:
    """Проверка установки и получения переменной."""
    app = TinyDBCli()

    app.do_SET("A 123")
    app.do_GET("A")

    captured = capsys.readouterr()
    assert "123" in captured.out


def test_get_undefined(capsys: CaptureFixture) -> None:
    """Проверка получения неустановленной переменной."""
    app = TinyDBCli()

    app.do_GET("A")

    captured = capsys.readouterr()
    assert "NULL" in captured.out


def test_simple_transaction(capsys: CaptureFixture) -> None:
    """Проверка создания переменной внутри транзакции."""
    run_multiple_commands(
        """
BEGIN
SET A 222
COMMIT
GET A""",
    )

    captured = capsys.readouterr()
    assert "222" in captured.out


def test_var_change_in_transaction(capsys: CaptureFixture) -> None:
    """Проверка изменения переменной внутри транзакции."""
    run_multiple_commands(
        """
SET A 10
BEGIN
SET A 20
COMMIT
GET A""",
    )

    captured = capsys.readouterr()
    assert "20" in captured.out


def test_rollback_in_transactions(capsys: CaptureFixture) -> None:
    """Проверка отката во вложенных транзакциях."""
    run_multiple_commands(
        """
BEGIN
SET A 10
BEGIN
SET A 20
BEGIN
SET A 30
GET A
ROLLBACK
GET A
COMMIT
GET A
20""",
    )

    captured = capsys.readouterr()
    assert "30" in captured.out
    assert "20" in captured.out


def test_unset(capsys: CaptureFixture) -> None:
    """Проверка получения переменной."""
    app = TinyDBCli()

    app.do_SET("A 222")
    app.do_GET("A")
    app.do_UNSET("A")
    app.do_GET("A")

    captured = capsys.readouterr()
    assert "222" in captured.out
    assert "NULL" in captured.out


def test_unset_undefined_var(capsys: CaptureFixture) -> None:
    """Проверка удаления несуществующей переменной."""
    app = TinyDBCli()

    app.do_UNSET("A")

    captured = capsys.readouterr()
    assert "" in captured.out


def test_unset_in_transaction(capsys: CaptureFixture) -> None:
    """Проверка удаления переменной внутри транзакции."""
    run_multiple_commands(
        """
BEGIN
SET A 111
UNSET A
COMMIT
GET A""",
    )

    captured = capsys.readouterr()
    assert "NULL" in captured.out


def test_count(capsys: CaptureFixture) -> None:
    """Проверка подсчета значений."""
    run_multiple_commands(
        """
SET A 10
SET B 10
BEGIN
SET C 10
COUNTS 10""",
    )

    captured = capsys.readouterr()
    assert "3" in captured.out


def test_find(capsys: CaptureFixture) -> None:
    """Проверка подсчета значений."""
    run_multiple_commands(
        """
SET A 10
SET B 10
SET C 20
BEGIN
SET D 10
FIND 10""",
    )

    captured = capsys.readouterr()
    assert "D A B" in captured.out


def test_command_need_argument_decorator() -> None:
    """Проверка декоратора, следящего за передачей аргумента в команду."""
    app = TinyDBCli()

    with pytest.raises(UserInputError) as excinfo:
        app.do_UNSET("")

    assert "для команды не хватает 1 аргумент(а/ов)" in str(excinfo.value)
