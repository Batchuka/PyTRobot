# pytrobot/__init__.py

import logging
import builtins

from pytrobot.starter import Starter
from pytrobot.dispatcher import Dispatcher
from pytrobot.performer import Performer
from pytrobot.handler import Handler
from pytrobot.finisher import Finisher
from pytrobot.transaction import Transaction
from pytrobot.assets import Assets

__all__ = ['Assets', 'Starter', 'Dispatcher', 'Performer', 'Handler', 'Finisher', 'Transaction']


def print_pytrobot():
    print("  _____        _______          _")
    print(" |  __ \__   _|__   __|        | |     o   _")
    print(" | |__) \ \ / /  | |_ ___  ___ | |__  _|_ | |__")
    print(" |  ___/ \   /   | | V __|/ _ \|  _ \/   \|  __|")
    print(" | |      | |    | |  /  | |_| | |_)( * * ) |")
    print(" |_|      |_|    |_|__|   \___/|____/\---/|_|")
    print(" ____________________________________________")
    print("|____________________________________________|")
    print("  -- Transactional State Robot for Python --")
    print("               Copyright © 2023")
    print("\n\n")

print_pytrobot()


class Logger:
    handle = None

    @staticmethod
    def setup():
        if Logger.handle is None:
            Logger.handle = logging.getLogger('pytrobot')
            Logger.handle.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s  %(levelname)s  %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            Logger.handle.addHandler(handler)

    @staticmethod
    def log(message, level=logging.INFO):
        Logger.setup()
        Logger.handle.log(level, message)  # type: ignore

def pytrobot_print(*args, **kwargs):
    message = " ".join(map(str, args))
    Logger.log(message, level=kwargs.get('level', logging.INFO))

# Substituir a função print padrão
builtins.print = pytrobot_print
