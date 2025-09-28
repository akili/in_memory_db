from _pytest.capture import CaptureFixture

from main import TinyDB


def test_eof_exit(capsys: CaptureFixture) -> None:
    """Проверка работы ctrl+d."""
    app = TinyDB()

    app.do_EXIT()

    captured = capsys.readouterr()
    assert "Пока!" in captured.out
