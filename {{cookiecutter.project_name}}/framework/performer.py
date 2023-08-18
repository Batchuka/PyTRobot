
"""
"""
from framework.robot import Robot, State
from framework.config import Config
from framework.transaction import Transaction
from framework.utils import *


@apply_decorator_to_all_methods(handle_exceptions)
@apply_decorator_to_all_methods(with_logging)
class Performer(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.PERFORMER

    def on_entry(self):

        # lógicas para iniciar o performer
        print("...")

    def execute(self):

        # lógicas alvo do performer
        print("...")

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER
