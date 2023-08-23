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
class Controller(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.CONTROLLER

    def on_entry(self):

        # Inicia tudo que precisará para executar a tarefa do Controller
        Config.set_class(MakeDatabaseConfig)
        self.mysql_hub = MysqlDB('host', 'user', 'password', 'database2')
        self.queue_verifica_radar = Queue('queue_url', 'region')

    def execute(self):

        Transaction

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        # Define your logic to determine the next state
        if True:
            self.next_state = State.CONTROLLER
        elif False:
            self.next_state = State.FINISHER
        elif False:
            self.next_state = State.PERFORMER
        else:
            self.next_state = State.DISPATCHER
