from abc import ABC, abstractmethod
from typing import Callable, Protocol, Sequence


class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...

class Formatter(ABC):
    @abstractmethod
    def format(self, items: Sequence[SupportsStr]) -> str:
        pass


def with_affix(prefix: str, suffix: str) -> Callable[..., Callable[..., str]]:
    """Decorator that adds a pre- or suffix to the string returned by the decorated function"""
    def inner(format_func) -> Callable[..., str]:
        def wrapper(*args, **kwargs) -> str:
            return prefix + format_func(*args, **kwargs) + suffix
        return wrapper
    return inner


class NewItemFormatter(Formatter):
    """i.e.: "New Exams: Exam1, Exam2" """

    item_name_singular: str
    item_name_plural: str

    def __init__(self, item_name_singular = 'Exam', item_name_plural = 'Exams') -> None:
        self.item_name_singular = item_name_singular
        self.item_name_plural = item_name_plural

    def format(self, items: Sequence[SupportsStr]) -> str:
        if len(items) == 0:
            return f"No new {self.item_name_singular}"
        elif len(items) == 1:
            return f"New {self.item_name_singular}: \n" + "\n".join(map(str, items))
        else:
            return f"New {self.item_name_plural}: \n" + "\n".join(map(str, items))


class SimpleFormatter(Formatter):
    """formats given items separated by given separator"""
    
    separator: str

    def __init__(self, separator: str = '\n') -> None:
        self.separator = separator

    @with_affix(prefix='', suffix='\n')
    def format(self, items: Sequence[SupportsStr]) -> str:
        return self.separator.join(map(str, items))
