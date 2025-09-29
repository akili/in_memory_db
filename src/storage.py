from contextlib import suppress

from .exceptions import StorageLogicError


class TinyDB:
    """Очень простая in-memory база данных."""

    NULL = "NULL"

    @property
    def upper_data_layer(self) -> dict:
        """Получение слоя данных или данныx самой верхней транзакции."""
        return self._storage[-1]

    def __init__(self) -> None:
        self._storage = [{}]

    def set(self, key: str, value: str) -> None:
        """Установить значение переменной."""
        self.upper_data_layer[key] = value

    def unset(self, key: str) -> None:
        """Удаление переменной."""
        if len(self._storage) == 1:
            with suppress(KeyError):
                del self.upper_data_layer[key]
        else:
            # мы внутри транзакции, если ключ просто удалить, при коммите
            # действие потеряется, поэтому помечаем его нулом
            self.upper_data_layer[key] = self.NULL

    def get(self, key: str) -> str:
        """Получить значение переменной."""
        for layer in reversed(self._storage):
            if key in layer:
                return layer[key]
        return self.NULL

    def begin_transaction(self) -> None:
        """Начать транзакцию."""
        self._storage.append({})

    def rollback_transaction(self) -> None:
        """Откатить последнюю транзакцию."""
        if len(self._storage) == 1:
            raise StorageLogicError("Нет ни одной транзакции для отката")
        self._storage.pop()

    def commit_transaction(self) -> None:
        """Зафиксировать текущую транзакцию."""
        if len(self._storage) == 1:
            raise StorageLogicError("Нет ни одной транзакции для коммита")
        # Реальные базы редко удаляют что-то сразу, можно было просто слить
        # нулы и не переживать о потери памяти
        for key, value in self._storage.pop().items():
            if value == self.NULL:
                with suppress(KeyError):
                    del self.upper_data_layer[key]
            else:
                self.upper_data_layer[key] = value

    def counts(self, searched_value: str) -> int:
        """Подсчет сколько раз данные значение встретились в базе данных."""
        cnt = 0
        for layer in self._storage:
            for var_value in layer.values():
                if var_value == searched_value:
                    cnt += 1
        return cnt

    def find(self, searced_value: str) -> str:
        """Поиск ключей по значению."""
        keys = []
        # reversed, чтобы переменныe в транзакции шли первыми
        for layer in reversed(self._storage):
            for key, value in layer.items():
                if value == searced_value:
                    keys.append(key)
        return " ".join(keys)
