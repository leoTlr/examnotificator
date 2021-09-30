from abc import ABC, abstractmethod
from typing import Protocol

from examnotificator.fetching.common import ExamFetcher
from examnotificator.model import Exam
from examnotificator.repo import ExamRepo


class NotificationStrategy(ABC):
    
    @abstractmethod
    def process(self) -> set[Exam]:
        pass


class ExamSetComparator(Protocol):
    def __call__(self, lhs: set[Exam], rhs: set[Exam]) -> set[Exam]: 
        ...


diff_to_old_comparator: ExamSetComparator = \
    lambda old_state, new_state: new_state.difference(old_state)


class FetchCompareStrategy(NotificationStrategy):
    """compares state of repo and results from fetching with given comparator"""
    repo: ExamRepo
    fetcher: ExamFetcher
    comparator: ExamSetComparator

    def __init__(self, repo: ExamRepo, fetcher: ExamFetcher, comparator: ExamSetComparator = diff_to_old_comparator) -> None:
        self.repo = repo
        self.fetcher = fetcher
        self.comparator = comparator

    def process(self) -> set[Exam]:
        old_state = self.repo.get()
        new_state = self.fetcher.execute()
        return self.comparator(old_state, new_state)


class AllExamsStrategy(NotificationStrategy):
    """gives out all exams in repo"""
    repo: ExamRepo

    def __init__(self, repo: ExamRepo) -> None:
        self.repo = repo

    def process(self) -> set[Exam]:
        return self.repo.get()
