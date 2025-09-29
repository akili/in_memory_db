import io
import sys

from _pytest.capture import CaptureFixture

from main import TinyDB


def run_multiple_commands(commands: str) -> None:
    """Передаем пачку комманд в приложение."""
    app = TinyDB()
    stdin_backup = sys.stdin
    sys.stdin = io.StringIO(commands)
    app.cmdloop()
    sys.stdin = stdin_backup


def test_eof_exit(capsys: CaptureFixture) -> None:
    """Проверка работы ctrl+d."""
    app = TinyDB()

    app.do_EXIT()

    captured = capsys.readouterr()
    assert "Пока!" in captured.out


def test_get_command(capsys: CaptureFixture) -> None:
    """Проверка установки переменной."""
    app = TinyDB()

    app.do_GET("A")

    captured = capsys.readouterr()
    assert "NULL" in captured.out


def test_set_command(capsys: CaptureFixture) -> None:
    """Проверка получения переменной."""
    app = TinyDB()

    app.do_SET("A 123")
    app.do_GET("A")

    captured = capsys.readouterr()
    assert "123" in captured.out


def test_simple_transaction(capsys: CaptureFixture) -> None:
    """Проверка транзакции."""
    run_multiple_commands(
        """
BEGIN
SET A 222
COMMIT
GET A""",
    )

    captured = capsys.readouterr()
    assert "222" in captured.out


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
