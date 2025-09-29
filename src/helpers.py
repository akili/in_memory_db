from functools import wraps
from typing import Callable

from .exceptions import UserInputError


def command_need_arguments(required: int) -> Callable:
    """Проверяем, что в команду передается нужное число аргументов."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple[str]) -> Callable:
            provided = len(args[1])
            if provided < required:
                missing = required - provided
                msg = f"для команды не хватает {missing} аргумент(а/ов)"
                raise UserInputError(msg)
            return func(*args)

        return wrapper

    return decorator
