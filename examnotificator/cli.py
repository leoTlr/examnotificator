from argparse import ArgumentParser
from pathlib import Path

from examnotificator.config import OpMode

def get_parser() -> ArgumentParser:
    parser = ArgumentParser("examnotificator")

    opmode_group = parser.add_mutually_exclusive_group(required=False)
    opmode_group.add_argument(
        "--new", action="store_const", const=OpMode.NEW, dest='opmode',
        help="fetch and show new exams since last fetch (default)")
    opmode_group.add_argument(
        "--saved", action="store_const", const=OpMode.SAVED, dest='opmode',
        help="show all saved exams without fetching")
    opmode_group.add_argument(
        "--fetch", action='store_const', const=OpMode.FETCH, dest='opmode',
        help='only fetch exams without saving them')
    opmode_group.add_argument(
        "--list-plugins-notificators", action="store_const", const=OpMode.LIST_PLUGINS_NOTIFICATOR, dest='opmode',
        help="list all loadable notificator plugins"
    )
    # opmode_group.add_argument(
    #     "--fetch", action='store_const', const=OpMode.FETCH, dest='opmode',
    #     help='only fetch exams')
    # opmode_group.add_argument(
    #     "--fetch-save", action='store_const', const=OpMode.FETCH_SAVE, dest='opmode',
    #     help='fetch exams and save them')

    # parser.add_argument(
    #     "--notify-desktop", action="store_true", 
    #     help="show desktop notification via dbus")
    parser.add_argument(
        "--config", type=Path, metavar='PATH',
        help="path to configuration file")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, 
        help='-v=info, -vv=debug')

    parser.add_argument(
        "-f", "--fetcher", 
        help="name of fetcher plugin to use")
    
    return parser