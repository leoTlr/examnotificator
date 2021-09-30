from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional, final

import stevedore.driver     # type: ignore
import stevedore.exception  # type: ignore

logger = logging.getLogger(__name__)


class PluginError(Exception):
    
    def __init__(self, plugin: "Plugin", *args: object) -> None:
        self.plugin = plugin
        super().__init__(*args)

    def __str__(self) -> str:
        return f'error in plugin "{self.plugin.name}": {super().__str__()}'


class Plugin(ABC):
    """Base class for plugins"""

    @abstractmethod
    def _run(self) -> Any:
        ...

    @property
    def name(self) -> str:
        """override this in subclass if plugin name != class name """
        return self.__class__.__name__

    @final
    def execute(self) -> Any:
        try:
            return self._run()
        except Exception as e:
            logger.exception(f'while executing plugin code for plugin "{self.name}", an exception occured. Traceback:')
            raise PluginError from e


plugin_load_failure_callback = lambda mgr, entrypoint, exception: \
    logger.error(f'error loading plugin "{entrypoint}": {exception}')

plugin_missing_entrypoints_callback = lambda items: \
    logger.warning(f'could not find entrypoints for plugins: {", ".join(items)}')

def load_single_plugin(name: str, namespace: str) -> Optional[Plugin]:
    try:
        mgr = stevedore.driver.DriverManager(
            namespace = namespace,
            name = name,
        )
        try:
            return mgr.driver()
        except Exception as e:
            logger.exception(f'while trying to invoke plugin "{name}" an exception occured. Traceback:')
            logger.warning(f'skip loading plugin "{name}"')
    except stevedore.exception.NoMatches as e:
        logger.warning(f'did not find plugin with name "{name}" in namespace "{namespace}": {e}')
    
    return None

def load_multiple_plugins(names: Iterable[str], namespace: str) -> list[Plugin]:
    return list((plugin for plugin in (load_single_plugin(name, namespace) for name in names) if plugin is not None))
