
"""
"""
from framework.robot import *
from framework.config import *
from framework.utils import *


@apply_decorator_to_all_methods(handle_exceptions)
@apply_decorator_to_all_methods(with_logging)
class Starter(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.STARTER

    def on_entry(self):

        # lógicas para iniciar o starter
        print("...")

    def execute(self):

        # lógicas alvo do starter
        print("...")

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER
