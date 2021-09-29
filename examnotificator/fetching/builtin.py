from typing import Optional

from examnotificator.fetching.common import ExamFetcher
from examnotificator.model import Exam


class DummyFetcher(ExamFetcher):
    """ returns given exams """
    
    exams: set[Exam]

    def __init__(self, exams: Optional[set[Exam]] = None) -> None:
        self.exams = exams or set()
        super().__init__()

    def fetch(self) -> set[Exam]:
        return self.exams
