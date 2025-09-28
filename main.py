import cmd
from typing import Any


class TinyDB(cmd.Cmd):
    """Очень простая консольная in-memory БД."""

    intro = (
        "Добро пожаловать в TinyDB! Введите help или ? для списка команд.\n"
    )
    prompt = "tiny_db> "

    def __init__(self) -> None:
        super().__init__()
        self.storage = {}

    def run(self, intro: Any | None = None) -> None:
        """REPL для приложения."""
        try:
            super().cmdloop(intro=intro)  # noqa: WPS613
        except KeyboardInterrupt:
            # Выход по ctrl+c
            self.do_EXIT()

    def do_EOF(self, _: str) -> bool:
        """Выйти по ctrl+d."""
        return self.do_EXIT()

    def do_EXIT(self, _: str | None = None) -> bool:
        """Выйти по команде."""
        print("\nПока!")
        return True


if __name__ == "__main__":
    TinyDB().run()
