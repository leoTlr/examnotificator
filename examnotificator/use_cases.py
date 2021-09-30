import logging
from abc import ABC, abstractmethod
from typing import Iterable

from examnotificator.fetching.common import ExamFetcher
from examnotificator.notification.common import Notificator, SupportsStr
from examnotificator.repo import ExamRepo

logger = logging.getLogger(__name__)


class UseCase(ABC):
    
    @abstractmethod
    def execute(self, repo: ExamRepo, fetcher: ExamFetcher, notificators: Iterable[Notificator]) -> None:
        ...

    @staticmethod
    def notify(items: set[SupportsStr], notificators: Iterable[Notificator]) -> None:
        for notificator_plugin in notificators:
            notificator_plugin.update(items)
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


class ListNotificatorPlugins(UseCase):
    """Output all names of loaded notificator plugins"""

    def execute(self, repo: ExamRepo, fetcher: ExamFetcher, notificators: Iterable[Notificator]) -> None:
        names = {notificator.name for notificator in notificators}
        self.notify(names, notificators)
