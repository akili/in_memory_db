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

    def cmdloop(self, intro: Any | None = None) -> None:
        """REPL для приложения."""
        try:
            super().cmdloop(intro=intro)
        except KeyboardInterrupt:
            # Выход по ctrl+c
            print("\nПока!")

    def do_EOF(self, _: str) -> bool:  # noqa: N802
        """Выйти по ctrl+d."""
        print("\nПока!")
        return True


if __name__ == "__main__":
    TinyDB().cmdloop()
