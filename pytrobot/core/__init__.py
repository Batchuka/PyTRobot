# pytrobot/__init__.py
import builtins
import os
import sys
import importlib

from pytrobot.core.singleton import Singleton
from pytrobot.core.feature.logging import print_pytrobot_banner
from pytrobot.core.feature.config import ConfigManager
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.state_strategy import StateStrategy
from pytrobot.core.strategy.orchestrator_strategy import OrchastratorStrategy

class PyTRobotNotInitializedException(Exception):
    """Exceção para ser levantada quando o PyTRobot não está instanciado."""
    pass

class PyTRobot(metaclass=Singleton):
    """Classe principal do pytrobot, implementada como um Singleton."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PyTRobot, cls).__new__(cls)
        return cls._instance

    def __init__(self, directory: str):
        if not hasattr(self, '_initialized'):
            self._initialize(directory)

    def _initialize(self, directory: str):
        print_pytrobot_banner()

        # Inicializa o gerenciador de configurações e carrega o arquivo de configuração
        self.config_manager = ConfigManager()
        self.config_manager.load_config(directory)

        # Carrega a estratégia do arquivo de configuração
        strategy_name = self.config_manager.get_config("strategy")
        if not strategy_name:
            raise ValueError("Strategy not specified in configuration.")

        self.strategy = self.load_strategy(strategy_name)
        self.strategy.initialize()

        # Guarda o diretório base e o caminho do diretório src
        self.base_directory = directory
        self.src_path = os.path.join(directory, 'src')
        sys.path.insert(0, str(self.src_path))

        # Importa todos os arquivos do diretório src
        if os.path.exists(self.src_path):
            self.import_all_files()
        else:
            raise FileNotFoundError("'src' directory not found.")

        self._initialized = True

    def start(self):
        self.strategy.start()

    def load_strategy(self, strategy_name: str) -> ApplicationStrategy:
        """
        Loads the appropriate strategy based on the configuration.
        """
        if strategy_name == "state":
            return StateStrategy()
        elif strategy_name == "orchestrator":
            return OrchastratorStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def import_all_files(self):
        """
        Imports all Python modules in the specified directory.
        """
        base_package = self._get_base_package()
        for file in os.listdir(self.src_path):
            if file.endswith(".py") and file not in ["__init__.py", "__main__.py"]:
                module_name = file[:-3]  # Remove .py
                importlib.import_module(f'{base_package}.src.{module_name}')

    def _get_base_package(self) -> str:
        """
        Extracts the base package name from the given src path.
        Assumes the base package is the directory name just before 'src'.
        """
        parts = self.src_path.split(os.sep)
        if 'src' in parts:
            return parts[parts.index('src') - 1]
        raise ValueError("Invalid src path: 'src' directory not found in path")

    def initialize_application(self):
        """
        Initializes the application by setting up the strategy
        and importing necessary modules.
        """
        self.start()

