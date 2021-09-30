import logging
from abc import ABC, abstractmethod
from typing import Iterable

from examnotificator.fetching.common import ExamFetcher
from examnotificator.model import Exam
from examnotificator.notification.common import Notificator
from examnotificator.repo import ExamRepo

logger = logging.getLogger(__name__)


class UseCase(ABC):
    
    @abstractmethod
    def execute(self, repo: ExamRepo, fetcher: ExamFetcher, notificators: Iterable[Notificator]) -> None:
        ...

    @staticmethod
    def notify(exams: set[Exam], notificators: Iterable[Notificator]) -> None:
        for notificator_plugin in notificators:
            notificator_plugin.add_exams(exams)
            notificator_plugin.execute()


class NotifySaved(UseCase):
    """ Output all exams in given repo"""

    def execute(self, repo: ExamRepo, _: ExamFetcher, notificators: Iterable[Notificator]) -> None:
        notification_exams = repo.get()
        self.notify(notification_exams, notificators)


class NotifyNew(UseCase):
    """ Output new exams since last fetch """

    def execute(self, repo: ExamRepo, fetcher: ExamFetcher, notificators: Iterable[Notificator]) -> None:
        old_state = repo.get()
        new_state = fetcher.execute(exit_on_fail=True)
        notification_exams = new_state.difference(old_state)
        self.notify(notification_exams, notificators)

