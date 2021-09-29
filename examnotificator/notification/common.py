from abc import abstractmethod
from typing import Optional, final

from examnotificator.model import Exam
from examnotificator.plugin import Plugin


class NotificatorError(Exception):
    ...

class Notificator(Plugin):
    """ 
    Base class for a notificator plugin. 
    """

    exams: set[Exam]

    def __init__(self, exams: Optional[set[Exam]] = None):
        self.exams = exams or set()
        super().__init__()

    @final
    def _run(self) -> None:
        return self.notify()

    def add_exams(self, exams: set[Exam]) -> None:
        self.exams.update(exams)

    @abstractmethod
    def notify(self) -> None:
        ...
