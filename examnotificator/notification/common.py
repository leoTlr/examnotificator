from abc import abstractmethod
from typing import Iterator, Optional, final, Protocol, Generic, TypeVar
from collections.abc import MutableSet

from examnotificator.model import Exam
from examnotificator.plugin import Plugin


class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...


class NotificatorError(Exception):
    ...


T = TypeVar('T', bound=SupportsStr)
class Notificator(Plugin, Generic[T], MutableSet):
    """ 
    Base class for a notificator plugin. 
    """

    items: MutableSet[T]

    def __init__(self, items: Optional[MutableSet[T]] = None):
        self.items = items or set()
        super().__init__()

    @abstractmethod
    def notify(self) -> None:
        ...

    @final
    def _run(self) -> None:
        return self.notify()

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, item: object) -> bool:
        return item in self.items

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def update(self, items: MutableSet[T]) -> None:
        self.items |= items

    def add(self, item: T) -> None:
        self.items.add(item)

    def discard(self, item: T) -> None:
        return super().discard(item)

