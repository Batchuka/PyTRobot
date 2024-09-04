# pytrobot/__init__.py
import builtins
import os
import sys
import importlib
from typing import Optional, Dict

from pytrobot.core.singleton import Singleton
from pytrobot.core.feature.logging import print_pytrobot_banner
from pytrobot.core.feature.config import ConfigManager
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.state.concrete import StateStrategy
from pytrobot.core.strategy.celery.concrete import CeleryStrategy

class PyTRobotNotInitializedException(Exception):
    """Exceção para ser levantada quando o PyTRobot não está instanciado."""
    pass

class PyTRobot(metaclass=Singleton):
    """Classe principal do pytrobot, implementada como um Singleton."""
    _instance = None

    def __init__(self, directory: Optional[str] = None, strategies: Optional[Dict[str, ApplicationStrategy]] = None):
        """
        Inicializa o PyTRobot. O diretório e as estratégias são opcionais.
        """
        if not hasattr(self, '_initialized'):
            if directory:
                self._initialize(directory, strategies)
            else:
                print("Nenhum diretório de projeto fornecido. Inicialização mínima.")
                self.strategies = strategies or {}
                self._initialized = True

    def _initialize(self, directory: str, strategies: Optional[Dict[str, ApplicationStrategy]] = None):

        print_pytrobot_banner()

        self.load_config(directory)
        self.load_src(directory)
        
        # Se estratégias foram passadas como argumento, use-as. Caso contrário, carregue conforme a configuração.
        if strategies:
            self.strategies = strategies
        else:
            self.strategies = {}
            self.load_strategies()

        self._initialized = True

    def _instantiate_strategy(self, strategy_name: str) -> ApplicationStrategy:
        """Instancia a estratégia com base no nome fornecido"""
        if strategy_name == "state":
            return StateStrategy()
        elif strategy_name == "orchestrator":
            return CeleryStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def _get_base_package(self) -> str:
        """Extrai o nome do pacote base do caminho do src"""
        parts = self.src_path.split(os.sep)
        if 'src' in parts:
            return parts[parts.index('src') - 1]
        raise ValueError("Invalid src path: 'src' directory not found in path")

    def _import_all_files(self):
        """Importa todos os módulos Python no diretório especificado"""
        base_package = self._get_base_package()
        for file in os.listdir(self.src_path):
            if file.endswith(".py") and file not in ["__init__.py", "__main__.py"]:
                module_name = file[:-3]  # Remove .py
                importlib.import_module(f'{base_package}.src.{module_name}')

    def load_config(self, directory: str):
        """Carrega o arquivo de configuração"""
        self.config_manager = ConfigManager()
        self.config_manager.load_config(directory)

    def load_src(self, directory: str):
        """Carrega todos os módulos do diretório 'src'"""
        self.base_directory = directory
        self.src_path = os.path.join(directory, 'src')
        sys.path.insert(0, str(self.src_path))

        if os.path.exists(self.src_path):
            self._import_all_files()
        else:
            raise FileNotFoundError("'src' directory not found.")

    def load_strategies(self):
        """Carrega a estratégia com base na configuração"""
        strategy_name = self.config_manager.get_config("strategy")
        if not strategy_name:
            raise ValueError("Strategy not specified in configuration.")
        self.strategy = self._instantiate_strategy(strategy_name)

    def initialize_application(self):
        """Inicializa todas as estratégias carregadas"""
        for strategy in self.strategies.values():
            strategy.initialize()

    def start_application(self):
        """Inicia todas as estratégias carregadas"""
        for strategy in self.strategies.values():
            strategy.start()

    def stop_application(self):
        """Inicia todas as estratégias carregadas"""
        for strategy in self.strategies.values():
            strategy.stop()


