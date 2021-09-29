import logging
from abc import abstractmethod
from typing import Optional

from examnotificator.model import Exam
from examnotificator.plugin import Plugin

logger = logging.getLogger(__name__)


class FetchingError(Exception):
    msg: str
    url: Optional[str]

    def __init__(self, msg: str, url: Optional[str] = None) -> None:
        self.url = url
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        if self.url:
            return f"fetching from {self.url} failed: {self.msg}"
        return f"fetching failed: {self.msg}"


class ParsingError(Exception):
    msg: str
    parse_item: Optional[str]

    def __init__(self, msg: str, parse_item: Optional[str] = None) -> None:
        self.msg = msg
        self.parse_item = parse_item

    def __str__(self) -> str:
        if self.parse_item:
            return f'error while parsing "{self.parse_item}": {self.msg}'
        return f'error while parsing: {self.msg}'


class ExamFetcher(Plugin):
    """ 
    Base class for a fetcher plugin.
    """

    def _run(self) -> set[Exam]:
        return self.fetch()

    @abstractmethod
    def fetch(self) -> set[Exam]:
        ...

