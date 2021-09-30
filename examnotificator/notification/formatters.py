from abc import ABC, abstractmethod
from typing import Callable

from examnotificator.model import Exam


class ExamFormatter(ABC):
    @abstractmethod
    def format(self, exams: set[Exam]) -> str:
        pass


def with_affix(prefix: str, suffix: str) -> Callable[..., Callable[..., str]]:
    """Decorator that adds a pre- or suffix to the string returned by the decorated function"""
    def inner(format_func) -> Callable[..., str]:
        def wrapper(*args, **kwargs) -> str:
            return prefix + format_func(*args, **kwargs) + suffix
        return wrapper
    return inner


class NewSinceLastFetchFormatter(ExamFormatter):
    """i.e.: "new Exams: Exam1, Exam2" """
    def format(self, exams: set[Exam]) -> str:
        if len(exams) == 0:
            return "No new exams"
        elif len(exams) == 1:
            return "New exam: \n" + "\n".join(map(str, exams))
        else:
            return "New exams: \n" + "\n".join(map(str, exams))


class SimpleExamFormatter(ExamFormatter):
    """formats given exams separated by given separator"""
    separator: str

    def __init__(self, separator: str = '\n') -> None:
        self.separator = separator

    @with_affix(prefix='', suffix='\n')
    def format(self, exams: set[Exam]) -> str:
        return self.separator.join(map(str, exams))
