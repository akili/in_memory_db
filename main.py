import cmd
from contextlib import suppress
from typing import Any


class TinyDB(cmd.Cmd):
    """Очень простая консольная in-memory БД."""

    NULL = "NULL"

    intro = (
        "Добро пожаловать в TinyDB! Введите help или ? для списка команд.\n"
    )
    prompt = "tiny_db> "

    def __init__(self) -> None:
        super().__init__()
        self.storage = [{}]

    def run(self, intro: Any | None = None) -> bool | None:
        """REPL для приложения."""
        try:
            super().cmdloop(intro=intro)  # noqa: WPS613
        except KeyboardInterrupt:
            # Выход по ctrl+c
            return self.do_EXIT()

    def onecmd(self, line: str) -> bool:
        """Выводим ошибки, не закрывая приложение."""
        try:
            return super().onecmd(line)
        except RuntimeError as error:
            print("Ошибочка вышла:", error)
            return False

    def do_EOF(self, _: str) -> bool:
        """Выйти по ctrl+d."""
        return self.do_EXIT()

    def do_EXIT(self, _: str | None = None) -> bool:
        """Выйти по команде."""
        print("\nПока!")
        return True

    def do_SET(self, args: str) -> None:
        """Установить значение переменной."""
        try:
            db_key, key_value = args.split()
        except ValueError as err:
            raise RuntimeError(
                "Нужно ввести 2 аргумента: имя переменной и ее значение",
            ) from err
        self.storage[-1][db_key] = key_value

    def do_GET(self, key: str) -> None:
        """Получить значение переменной."""
        for layer in reversed(self.storage):
            if key in layer:
                print(layer[key])
                break
        else:
            print(self.NULL)

    def do_BEGIN(self, _: str) -> None:
        """Начать транзакцию."""
        self.storage.append({})

    def do_ROLLBACK(self, _: str) -> None:
        """Откатить последнюю транзакцию."""
        if len(self.storage) == 1:
            raise RuntimeError("Нет ни одной транзакции для отката")
        self.storage.pop()

    def do_COMMIT(self, _: str) -> None:
        """Зафиксировать последнюю транзакцию."""
        if len(self.storage) == 1:
            raise RuntimeError("Нет ни одной транзакции для коммита")
        # Реальные базы редко удаляют что-то сразу, можно было просто слить
        # нулы и не переживать о потери памяти
        for key, value in self.storage.pop().items():
            if value == self.NULL:
                with suppress(KeyError):
                    del self.storage[-1][key]
            else:
                self.storage[-1][key] = value

    def do_UNSET(self, key: str) -> None:
        """Удаление переменной."""
        if len(self.storage) == 1:
            with suppress(KeyError):
                del self.storage[-1][key]
        else:
            # мы внутри транзакции, если ключ просто удалить, при коммите
            # действие потеряется, поэтому просто помечаем его нулом
            self.storage[-1][key] = self.NULL


if __name__ == "__main__":
    TinyDB().run()
