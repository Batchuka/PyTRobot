# pytrobot/__init__.py

import logging
import builtins
from pytrobot.core.states import *
from pytrobot.core.transitions import *
from pytrobot.core.assets import Assets

__all__ = ['PyTRobot']

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
    print("\n".join(banner_lines))

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

def pytrobot_print(*args, **kwargs):
    """Função print personalizada para redirecionar para o logger."""
    message = " ".join(map(str, args))
    Logger.log(message, level=kwargs.get('level', logging.INFO))

class PyTRobot:
    """Classe principal do pytrobot, implementada como um Singleton."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PyTRobot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Se esta for a primeira instanciação, continue com a inicialização
        if not hasattr(self, '_initialized'):
            self._initialize()

    def _initialize(self):
        """Inicializa o PyTRobot."""

        print_pytrobot_banner()

        # Substituir a função print padrão do Python pela função pytrobot_print
        builtins.print = pytrobot_print

        # Aqui deve ser adicionada a lógica de inicialização do PyTRobot
        # Por exemplo, instanciar classes do usuário, injetar dependências, etc.

        self._initialized = True

# Exemplo de uso do PyTRobot
pytrobot_instance = PyTRobot()