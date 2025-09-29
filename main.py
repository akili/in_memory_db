import cmd
from typing import Any

from exceptions import StorageLogicError, UserInputError
from helpers import command_need_arguments
from storage import TinyDB


class TinyDBCli(cmd.Cmd):
    """Консольный интефейс к базе данных."""

    intro = (
        "Добро пожаловать в TinyDB! Введите help или ? для списка команд.\n"
    )
    prompt = "tiny_db> "

    def __init__(self) -> None:
        super().__init__()
        self._database = TinyDB()

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
        except (UserInputError, StorageLogicError) as error:
            print("Ошибочка вышла:", error)
            return False

    def do_EOF(self, _: str) -> bool:
        """Выйти по ctrl+d."""
        return self.do_EXIT()

    def do_EXIT(self, _: str | None = None) -> bool:
        """Выйти по команде."""
        print("\nПока!")
        return True

    @command_need_arguments(2)
    def do_SET(self, args: str) -> None:
        """Команда для сохранения данных."""
        db_key, key_value = args.split()
        self._database.set(db_key, key_value)

    @command_need_arguments(1)
    def do_GET(self, key: str) -> None:
        """Команда для получения данных."""
        print(self._database.get(key))

    def do_BEGIN(self, _: str) -> None:
        """Команда старта транзакции."""
        self._database.begin_transaction()

    def do_ROLLBACK(self, _: str) -> None:
        """Команда отката транзакции."""
        self._database.rollback_transaction()

    def do_COMMIT(self, _: str) -> None:
        """Зафиксировать последнюю транзакцию."""
        self._database.commit_transaction()

    @command_need_arguments(1)
    def do_UNSET(self, key: str) -> None:
        """Команда для удаление данных."""
        self._database.unset(key)

    @command_need_arguments(1)
    def do_COUNTS(self, arg: str) -> None:
        """Команда подстчета данных."""
        print(self._database.counts(arg))

    @command_need_arguments(1)
    def do_FIND(self, arg: str) -> None:
        """Поиск ключей по значению."""
        print(self._database.find(arg))


if __name__ == "__main__":
    TinyDBCli().run()
