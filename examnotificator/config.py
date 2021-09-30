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

CONF_DEFAULT_FILEPATH: Path = Path.home() / Path('.config/examnotificator/examnotificator.yml')

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
    configurator.mapping.if_supplied('fetcher'): 'fetcher',
    configurator.mapping.if_supplied('opmode'): 'mode',
    'verbose': 'verbosity',
    'notify_desktop': 'notificators.dbus.notify',
    configurator.mapping.if_supplied('state_location'): 'repo.shelve.path',
}

def load_config(cmdargs: Namespace, config_file: Optional[Path] = CONF_DEFAULT_FILEPATH) -> configurator.Config:
    file_conf = configurator.Config.from_path(config_file, optional = True)
    
    global config
    config.merge(file_conf, {
        'fetcher': 'fetcher',
        'notificators': 'notificators'
    })

    config.merge(cmdargs, _cli_arg_mapping)
