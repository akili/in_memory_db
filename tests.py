import io
import sys

from _pytest.capture import CaptureFixture

from main import TinyDB


def test_exit_app(capsys: CaptureFixture) -> None:
    """Проверка работы ctrl+d."""
    shell = TinyDB()

    stdin_backup = sys.stdin
    sys.stdin = io.StringIO("\n")
    shell.cmdloop()
    sys.stdin = stdin_backup

    captured = capsys.readouterr()
    assert "Пока!" in captured.out
