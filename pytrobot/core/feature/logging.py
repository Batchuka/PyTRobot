# pytrobot/core/feature/logging.py
from enum import Enum
import logging
from typing import Literal

from pytrobot.core.singleton import Singleton

"""TODO
Adicionar essa modificação de cores no logger para dar acesso
como um recurso.
"""
from enum import Enum

class TerminalColor(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BLUE = '\033[94m'

def print_pytrobot_banner():
    """Exibe o banner do pytrobot."""
    banner_lines = [
        r"  _____        _______          _",
        r" |  __ \__   _|__   __|        | |     o   _",
        r" | |__) \ \ / /  | |_ ___  ___ | |__  _|_ | |__",
        r" |  ___/ \ V /   | | V __|/ _ \|  _ \/   \|  __|",
        r" | |      | |    | |  /  | |_| | |_)( * * ) |",
        r" |_|      |_|    |_|__|   \___/|____/\---/|_|",
        r" ____________________________________________",
        r"|____________________________________________|",
        r"      -- Transactional Robot for Python --    ",
        r"               Copyright © 2023",
        "\n\n"
    ]
    banner_text = "\n".join(banner_lines)
    print(f"{TerminalColor.BLUE}{banner_text}{TerminalColor.RESET}")

class Logger(metaclass=Singleton):
    """Logger customizado para o PyTRobot."""

    def _setup_logger(self, log_level, show_datetime, error_verbosity):
        self.logger = logging.getLogger('pytrobot')
        self.logger.setLevel(log_level)
        format_str = "%(message)s"
        if show_datetime:
            format_str = "%(asctime)s  %(levelname)s  %(message)s"

        formatter = logging.Formatter(format_str, datefmt="%d-%m-%Y %H:%M:%S")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.error_verbosity = error_verbosity

    def log(self, message, level=logging.INFO):
        color = TerminalColor.RESET.value
        if level == logging.ERROR:
            color = TerminalColor.RED.value
        elif level == logging.WARNING:
            color = TerminalColor.YELLOW.value
        elif level == logging.DEBUG:
            color = TerminalColor.BLUE.value
        
        self.logger.log(level, f"{color}{message}{TerminalColor.RESET.value}")

    def info(self, message):
        self.log(message, level=logging.INFO)

    def debug(self, message):
        self.log(message, level=logging.DEBUG)

    def error(self, message):
        self.log(message, level=logging.ERROR)