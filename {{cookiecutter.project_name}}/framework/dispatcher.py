from .robot import Robot
from .state import State
from .config import Config
from .transaction import Transaction
from .utils import *
"""
imports do framework  ↑
imports do usuário    ↓
"""


@apply_decorator_to_all_methods(handle_exceptions)
@apply_decorator_to_all_methods(with_logging)
class Dispatcher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.DISPATCHER

    def on_entry(self):

        # exemplo → result = MySQL.select('entidade', "id_status='2'")
        pass

    def execute(self):

        # lógicas alvo do dispatcher
        print("lógicas alvo do dispatcher")

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER
