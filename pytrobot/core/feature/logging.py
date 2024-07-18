from enum import Enum
import logging

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

def WithLog(func):
    """
    Um decorator que registra a chamada de uma função com informações de depuração.

    :param func: A função a ser decorada.
    """

    def wrapper(self, *args, **kwargs):
        # Logger.log(f"{self.current_state}.{func.__name__}", logging.DEBUG)
        print(f"{self.current_state}.{func.__name__}", logging.DEBUG)
        func(self, *args, **kwargs)
    return wrapper

def print_pytrobot_banner():
    """Exibe o banner do pytrobot."""
    banner_lines = [
        "  _____        _______          _",
        " |  __ \__   _|__   __|        | |     o   _",
        " | |__) \ \ / /  | |_ ___  ___ | |__  _|_ | |__",
        " |  ___/ \ V /   | | V __|/ _ \|  _ \/   \|  __|",
        " | |      | |    | |  /  | |_| | |_)( * * ) |",
        " |_|      |_|    |_|__|   \___/|____/\---/|_|",
        " ____________________________________________",
        "|____________________________________________|",
        "  -- Transactional State Robot for Python --",
        "               Copyright © 2023",
        "\n\n"
    ]
    print(BLUE + "\n".join(banner_lines) + RESET)

def pytrobot_print(*args, **kwargs):
    """Função print personalizada para redirecionar para o logger."""
    message = " ".join(map(str, args))
    Logger.log(message, level=kwargs.get('level', logging.INFO))

class Logger:
    """Um logger personalizado para o pytrobot."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._setup_logger()
        return cls._instance

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger('pytrobot')
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def log(message, level=logging.INFO):
        logger = Logger.get_instance()
        logger.log(level, message)