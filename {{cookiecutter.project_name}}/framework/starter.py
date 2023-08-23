from .robot import Robot
from .state import State
from .config import Config
from .transaction import Transaction
from .utils import *
"""
imports do framework  ↑
imports do usuário    ↓
"""
from make_database import MakeDatabaseConfig, MysqlDB
from make_aws import Queue


@apply_decorator_to_all_methods(handle_exceptions)
@apply_decorator_to_all_methods(with_logging)
class Starter(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.STARTER

    def on_entry(self):

        # Inicia tudo que precisará para executar a tarefa do Starter
        Config.set_class(MakeDatabaseConfig)
        self.mysql_rpa = MysqlDB('host', 'user', 'password', 'database1')

    def execute(self):

        # Exemplo : Log de execução no banco RPA
        self.mysql_rpa.insert('table', 'attributes', 'values')

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER
