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
class Finisher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.FINISHER

    def on_entry(self):

        # lógicas para iniciar o finisher
        print("...")

    def execute(self):

        # lógicas alvo para o finisher
        print("...")

    def on_error(self):

        delete_all_temp_files()
        logging.debug("I shit myself!")
        exit()

    def on_exit(self):

        delete_all_temp_files()
        logging.debug("I'll be back!")
        exit()
