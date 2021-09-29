import logging
from abc import ABC, abstractmethod
from typing import Iterable

from examnotificator.fetching.common import ExamFetcher
from examnotificator.model import Exam
from examnotificator.notification.common import Notificator
from examnotificator.notification.strategies import (AllExamsStrategy,
                                                     FetchCompareStrategy,
                                                     diff_to_old_comparator)
from examnotificator.plugin import PluginError
from examnotificator.repo import ExamRepo

logger = logging.getLogger(__name__)



class UseCase(ABC):
    
    def execute(self, repo: ExamRepo, fetcher: ExamFetcher, notificators: Iterable[Notificator]) -> None:
        
        try:
            exams: set[Exam] = self.get_exams(repo, fetcher)
        except Exception as e:
            logger.error(f'error while preparing exams for notification: {e}')
            raise e

        try:
            self.notify(exams, notificators)
        except PluginError as e:
            logger.error(f'{e}')

    @staticmethod
    def notify(exams: set[Exam], notificators: Iterable[Notificator]) -> None:
        for notificator in notificators:
            try:
                notificator.add_exams(exams)
                notificator.notify()
            except Exception as e:
                raise PluginError(notificator) from e
                

    @staticmethod
    @abstractmethod
    def get_exams(repo: ExamRepo, fetcher: ExamFetcher) -> set[Exam]:
        """Return the exams to be notified"""
        raise NotImplementedError


class NotifySaved(UseCase):
    """ Output all exams in given repo"""

    @staticmethod
    def get_exams(repo: ExamRepo, _: ExamFetcher) -> set[Exam]:
        return AllExamsStrategy(repo).process()


class NotifyNew(UseCase):
    """ Output new exams since last fetch """
    
    @staticmethod
    def get_exams(repo: ExamRepo, fetcher: ExamFetcher) -> set[Exam]:
        return FetchCompareStrategy(
            repo, fetcher, diff_to_old_comparator
        ).process()

