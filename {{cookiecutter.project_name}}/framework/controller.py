
"""
"""
from framework.robot import Robot, State
from framework.config import Config
from framework.transaction import Transaction
from framework.utils import *


@apply_decorator_to_all_methods(handle_exceptions)
@apply_decorator_to_all_methods(with_logging)
class Controller(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.CONTROLLER

    def on_entry(self):

        # lógicas para iniciar o controler
        print("lógicas para iniciar o controler")

    def execute(self):

        # lógicas alvo do controler
        print("lógicas alvo do controler")

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER
