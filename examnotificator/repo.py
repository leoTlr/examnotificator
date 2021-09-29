import shelve

from abc import ABC, abstractmethod
from typing import Callable
from pathlib import Path

from examnotificator.model import Exam

ExamFilterFunc = Callable[[Exam], bool]


class ExamRepo(ABC):
    
    @abstractmethod
    def get(self, exam_filter: ExamFilterFunc = lambda x: True) -> set[Exam]:
        pass

    @abstractmethod
    def save(self, exams: set[Exam], override: bool = False) -> None:
        pass


class MemRepo(ExamRepo):
    exams: set[Exam]

    def __init__(self, exams: set[Exam]) -> None:
        self.exams = exams

    def get(self, exam_filter: ExamFilterFunc = lambda x: True) -> set[Exam]:
        return set(filter(exam_filter, self.exams))

    def save(self, exams: set[Exam], override: bool = False) -> None:
        if override:
            self.exams.update(exams)
        else:
            self.exams = exams


class ShelveRepo(ExamRepo):
    """ Dumps data on file system using python shelve module """

    def __init__(self, path: Path) -> None:
        self.path = str(path)
        self._dict_key = 'exams'

    def save(self, exams: set[Exam], override: bool = False) -> None:
        with shelve.open(self.path) as db:
            if override or not self._dict_key in db:
                db[self._dict_key] = exams
            else:
                db[self._dict_key] = db[self._dict_key] | exams

    def get(self, exam_filter: ExamFilterFunc = lambda x: True) -> set[Exam]:
        try:
            with shelve.open(self.path) as db:
                exams = db[self._dict_key]
            return set(filter(exam_filter, exams))
        except KeyError:
            return set()
