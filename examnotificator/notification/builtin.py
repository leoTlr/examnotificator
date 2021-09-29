from sys import stdout
from typing import TextIO

import dbus  # type: ignore
from examnotificator.notification.common import Notificator
from examnotificator.notification.formatters import (
    NewSinceLastFetchFormatter, SimpleExamFormatter)


class NoOpNotificator(Notificator):
    """Does nothing"""

    def notify(self) -> None:
        return


class FileNotificator(Notificator):
    """writes message to (opened) file"""

    file: TextIO

    def __init__(self, file: TextIO) -> None:
        self.file = file
        super().__init__()

    def notify(self) -> None:
        msg = SimpleExamFormatter(separator = '\n').format(self.exams)
        self.file.write(msg)


class TerminalNotificator(FileNotificator):
    """prints msg to stdout"""

    def __init__(self) -> None:
        super().__init__(file=stdout)


class DbusNotificator(Notificator):
    """Shows desktop notifications on linux using dbus"""

    interface: dbus.Interface

    def __init__(self) -> None:
        self.interface = dbus.Interface(
            object = dbus.SessionBus().get_object(
                "org.freedesktop.Notifications", "/org/freedesktop/Notifications"
            ),
            dbus_interface="org.freedesktop.Notifications",
        )
        super().__init__()

    def notify(self) -> None:
        if len(self.exams) <= 0:
            return

        msg: str = NewSinceLastFetchFormatter().format(self.exams)

        self.interface.Notify(
            "", 0, "", "examnotificator", msg, [], {"urgency": 1}, 10000
        )
