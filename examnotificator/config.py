import configurator # type: ignore

from typing import Optional
from enum import Enum
from pathlib import Path
from argparse import Namespace

from examnotificator.use_cases import NotifyNew, NotifySaved, ListNotificatorPlugins, Fetch


class OpMode(Enum):
    NEW = NotifyNew
    SAVED = NotifySaved
    FETCH = Fetch
    LIST_PLUGINS_NOTIFICATOR = ListNotificatorPlugins


USER_CONF_DEFAULT_FILEPATH: Path = Path.home() / Path('.config/examnotificator/examnotificator.yml')

_defaults = configurator.Config({
    'mode': OpMode.NEW,
    'verbosity': 0,
    'plugin_namespaces': {
        'fetcher': 'examnotificator.plugins.fetchers',
        'notificators': 'examnotificator.plugins.notificators',
    },
    'repo': {
        'name': 'shelve', 
        'config': {
            'path': Path('.pickedb')
        }
    },
    'fetcher': {
        'name': 'dummy',
        'config': dict(),
    },
    'notificators': {
        'terminal': {'notify': True},
        'dbus': {'notify': True},
    },
})

config = _defaults

_cli_arg_mapping = {
    configurator.mapping.if_supplied('fetcher'): 'fetcher.name',
    configurator.mapping.if_supplied('opmode'): 'mode',
    'verbose': 'verbosity',
    'notify_desktop': 'notificators.dbus.notify',
}

def load_config(cli_args: Namespace, config_file: Optional[Path] = None) -> configurator.Config:
    """
    Populate module-level config object with cli and config file args.
    Precedence: cli > config file > defaults
    """

    config_file = config_file or USER_CONF_DEFAULT_FILEPATH
    file_conf = configurator.Config.from_path(config_file, optional = True)
    cli_conf = configurator.Config(cli_args)
    
    # module-global config object
    config.merge(file_conf)
    config.merge(cli_conf, _cli_arg_mapping)
