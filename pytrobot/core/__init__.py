# pytrobot/__init__.py
import builtins
import os
import sys
import importlib
from typing import Optional, Dict

from pytrobot.core.singleton import Singleton
from pytrobot.core.feature.logging import print_pytrobot_banner
from pytrobot.core.feature.config import ConfigManager
from pytrobot.core.feature.multithread import MultithreadManager
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.state.concrete import StateStrategy
from pytrobot.core.strategy.celery.concrete import CeleryStrategy

class PyTRobotNotInitializedException(Exception):
    """Exceção para ser levantada quando o PyTRobot não está instanciado."""
    pass

class PyTRobot(metaclass=Singleton):
    """Classe principal do pytrobot, implementada como um Singleton."""
    _instance = None

    def __init__(self, directory: str , strategies: Optional[list[str]] = None):
        """
        Inicializa o PyTRobot. O diretório e as estratégias são opcionais.
        """
        if not hasattr(self, '_initialized'):
            self._initialize(directory, strategies)


    def _initialize(self, directory: str, strategies: Optional[list[str]] = None):

        print_pytrobot_banner()

        self.load_config(directory)
        self.load_src(directory)
        
        # Se estratégias foram passadas como argumento, use-as. Caso contrário, carregue conforme a configuração.
        if strategies:
            self.strategies = strategies
        else:
            self.strategies = {}
            self.load_strategies()

        self.multithread_manager = MultithreadManager()

        self._initialized = True

    def _instantiate_strategies(self, strategy_names: list) -> list[ApplicationStrategy]:
        """Instancia uma lista de estratégias com base nos nomes fornecidos"""
        strategies = []
        
        for strategy_name in strategy_names:
            if strategy_name == "state":
                strategies.append(StateStrategy())
            elif strategy_name == "celery":
                strategies.append(CeleryStrategy())
            else:
                raise ValueError(f"Unknown strategy: {strategy_name}")

        return strategies

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

    def load_strategies(self, strategies: Optional[list[str]] = None):
        """Carrega as estratégias com base na lista de estratégias ou na configuração."""
        if strategies:
            # Instancia as estratégias passadas como strings
            self.strategies : list[ApplicationStrategy] = self._instantiate_strategies(strategies)
        else:
            # Carrega as estratégias da configuração
            strategy_name = self.config_manager.get_config("strategy")
            if not strategy_name:
                raise ValueError("Strategy not specified in configuration.")
            
            # Carrega a estratégia com base na configuração
            self.strategies : list[ApplicationStrategy] = self._instantiate_strategies(strategy_name)

    def monitor_threads(self):
        """Monitora as threads ativas e mantém o processo ativo enquanto houver threads."""
        import time
        while True:
            active_threads = self.multithread_manager.get_number_active_threads()
            if active_threads and active_threads == 0:
                print("Nenhuma thread ativa, encerrando o processo...")
                break
            time.sleep(10)

    def initialize_application(self):
        """Inicializa todas as estratégias carregadas"""
        for strategy in self.strategies:
            strategy.initialize()

    def start_application(self):
        """Inicia todas as estratégias carregadas"""
        for strategy in self.strategies:
            strategy.start()

        # Inicia o monitoramento das threads
        self.monitor_threads()

    def stop_application(self):
        """Inicia todas as estratégias carregadas"""
        for strategy in self.strategies:
            strategy.stop()


