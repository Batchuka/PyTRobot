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

    def __init__(self, directory: str):
        """
        Inicializa o PyTRobot. O diretório e as estratégias são opcionais.
        """
        if not hasattr(self, '_initialized'):
            self._initialize(directory)

    def _initialize(self, directory: str):

        print_pytrobot_banner()

        self.load_config(directory)
        self.load_src(directory)

        self.multithread_manager = MultithreadManager()

        # Verifica se há registros nos registries e adiciona as estratégias necessárias
        self._check_and_register_strategies()

        self._initialized = True

    def _check_and_register_strategies(self):
        """Verifica se há registros de tasks ou states e adiciona as estratégias necessárias."""
        from pytrobot.core.strategy.celery.task_registry import TaskRegistry
        from pytrobot.core.strategy.state.state_registry import StateRegistry

        self.strategies = []

        task_registry = TaskRegistry()
        state_registry = StateRegistry()

        # Adiciona a CeleryStrategy se houver tasks registradas
        if task_registry.get_all():
            self.strategies.append(CeleryStrategy())

        # Adiciona a StateStrategy se houver states registrados
        if state_registry.get_all():
            self.strategies.append(StateStrategy())

        # Caso não haja registros e nenhuma estratégia configurada, lança um erro
        if not self.strategies:
            raise ValueError("Nenhuma estratégia registrada ou especificada na configuração.")

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



"""
TODO: Retirei a posibilidade de passar argumentos de estratégia por hora. Agora é só no reconhecimento automático.
"""