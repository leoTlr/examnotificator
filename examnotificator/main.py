from __future__ import annotations  # can probably be removed in Python 3.11

import logging
import sys
from argparse import ArgumentError
from typing import Optional, cast

from configurator import Config  # type: ignore

from examnotificator.cli import get_parser
from examnotificator.config import OpMode, config, load_config
from examnotificator.fetching.common import ExamFetcher
from examnotificator.notification.common import Notificator
from examnotificator.plugin import load_multiple_plugins, load_single_plugin
from examnotificator.repo import ExamRepo, ShelveRepo
from examnotificator.use_cases import UseCase

logger = logging.getLogger(__name__)


def configure_logging(verbosity_level: int) -> None:

    verbosity = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
    if not verbosity_level in verbosity.keys():
        raise ArgumentError(None, f'verbosity has to be one of {list(verbosity.keys())}')

    logging.basicConfig(
        format="[%(levelname)-8s] %(asctime)s: %(message)s [%(filename)s]",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=verbosity[verbosity_level],
    )



class App:
    repo: ExamRepo
    fetcher: ExamFetcher
    notificators: list[Notificator]
    use_case: UseCase

    @classmethod
    def from_config(cls, config: Config) -> App:

        notificator_plugin_names = [
            str(key) for key, val in config.notificators.items() 
            if 'notify' in val and val['notify'] == True
        ]
        
        return cls()\
            .with_repo(ShelveRepo(config.repo.config.path))\
            .with_fetcher(config.fetcher.name, config.plugin_namespaces.fetcher)\
            .with_notificators(notificator_plugin_names, config.plugin_namespaces.notificators)\
            .for_use_case(config.mode)

    def with_repo(self, repo: ExamRepo) -> App:
        self.repo = repo
        return self

    def with_fetcher(self, name: str, namespace: str) -> App:
        fetcher: Optional[ExamFetcher] = cast(ExamFetcher, 
            load_single_plugin(name, namespace))
        if not isinstance(fetcher, ExamFetcher):
            logger.error(f'could not load requested fetcher plugin "{config.fetcher.name}"')
            sys.exit(-1)
        logger.info(f'successfully loaded fetcher plugin "{config.fetcher.name}"')
        self.fetcher = fetcher
        return self

    def with_notificators(self, names: list[str], namespace: str) -> App:
        notificators: list[Notificator] = cast(list[Notificator],
            load_multiple_plugins(names, namespace))
        logger.info(f'successfully loaded notificator plugins: {", ".join(plugin.name for plugin in notificators)}')
        self.notificators = notificators
        return self

    def for_use_case(self, mode: OpMode) -> App:
        self.use_case = mode.value()
        logger.info(f'performing use case {mode}')
        return self

    def execute(self):
        self.use_case.execute(self.repo, self.fetcher, self.notificators)



def main() -> None:
    arg_parser = get_parser()
    args = arg_parser.parse_args()
    configure_logging(args.verbose)

    if args.config:
        load_config(args, args.config)
    else:
        load_config(args)

    app = App.from_config(config)
    app.execute()

    